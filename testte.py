import   as ft
from datetime import datetime

def main(page: ft.Page):
    # Configurações da Janela
    page.title = "Calculadora de Compras"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # O SEGREDO PARA O TECLADO: Rolagem adaptativa!
    page.scroll = "adaptive" 
    
    # Controle de Estado
    estado = {"limite": 0.0, "total_gasto": 0.0, "produtos": []}

    # --- FUNÇÕES ---
    def atualizar_status():
        restante = estado["limite"] - estado["total_gasto"]
        lbl_status.value = f"Total: R${estado['total_gasto']:.2f} | Restante: R${restante:.2f}"
        page.update()

    def fechar_alerta(e):
        alerta.open = False
        page.update()

    alerta = ft.AlertDialog(
        title=ft.Text("Atenção", weight=ft.FontWeight.BOLD),
        content=ft.Text(""),
        actions=[ft.TextButton("OK", on_click=fechar_alerta)],
    )

    def mostrar_alerta(mensagem):
        alerta.content.value = mensagem
        page.dialog = alerta
        alerta.open = True
        page.update()

    def remover_item(item_ui, subtotal, prod_tuple):
        lista_produtos.controls.remove(item_ui)
        estado["total_gasto"] -= subtotal
        estado["produtos"].remove(prod_tuple)
        
        # Libera o campo limite se a lista esvaziar
        if not estado["produtos"] and estado["total_gasto"] == 0:
            ent_limite.disabled = False
            estado["limite"] = 0.0
            
        atualizar_status()

    def adicionar_produto(e):
        try:
            # Trava e registra o limite na primeira inserção
            if estado["limite"] == 0.0:
                if not ent_limite.value:
                    mostrar_alerta("Digite o valor disponível primeiro!")
                    return
                estado["limite"] = float(ent_limite.value.replace(",", "."))
                ent_limite.disabled = True

            nome = ent_produto.value.strip()
            preco = float(ent_preco.value.replace(",", "."))
            qtd = int(ent_qtd.value) if ent_qtd.value else 1
            subtotal = preco * qtd

            if not nome:
                mostrar_alerta("Digite o nome do produto!")
                return

            if estado["total_gasto"] + subtotal > estado["limite"]:
                mostrar_alerta("Esta compra ultrapassa o limite disponível!")
                return

            # Atualiza valores
            estado["total_gasto"] += subtotal
            prod_tuple = (nome, preco, qtd)
            estado["produtos"].append(prod_tuple)

            # Cria a linha visual do produto com botão de excluir
            texto_item = f"{nome} | R${preco:.2f} x {qtd} = R${subtotal:.2f}"
            
            # Usando ListTile nativo para visual moderno
            item_ui = ft.ListTile(
                title=ft.Text(texto_item, size=15),
                trailing=ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE, 
                    icon_color="red400",
                    tooltip="Excluir item"
                )
            )
            
            # Vincula a função de remoção ao botão
            item_ui.trailing.on_click = lambda e, ui=item_ui, sub=subtotal, pt=prod_tuple: remover_item(ui, sub, pt)
            
            lista_produtos.controls.append(item_ui)

            # Limpa e foca nos campos
            ent_produto.value = ""
            ent_preco.value = ""
            ent_qtd.value = "1"
            ent_produto.focus()

            atualizar_status()

        except ValueError:
            mostrar_alerta("Preencha os campos de valor com números válidos!")

    # --- ELEMENTOS DA INTERFACE ---
    lbl_titulo = ft.Text("CALCULADORA DE COMPRAS", weight=ft.FontWeight.BOLD, size=20)
    lbl_data = ft.Text(f"Data: {datetime.now().strftime('%d/%m/%Y - %H:%M')}", color=ft.colors.GREY_500, size=13)

    ent_limite = ft.TextField(label="Disponível", keyboard_type=ft.KeyboardType.NUMBER, prefix_text="R$ ")
    ent_produto = ft.TextField(label="Produto (Ex: Arroz)", text_transform=ft.TextCapitalization.WORDS)
    ent_preco = ft.TextField(label="Preço", keyboard_type=ft.KeyboardType.NUMBER, prefix_text="R$ ", expand=2)
    ent_qtd = ft.TextField(label="Qtd", value="1", keyboard_type=ft.KeyboardType.NUMBER, expand=1)

    linha_preco_qtd = ft.Row([ent_preco, ent_qtd])

    btn_add = ft.ElevatedButton(
        text="Adicionar Produto", 
        icon=ft.icons.ADD_SHOPPING_CART, 
        bgcolor=ft.colors.BLUE_700, 
        color=ft.colors.WHITE,
        on_click=adicionar_produto,
        height=50,
        expand=True
    )

    lbl_status = ft.Text("Total: R$0.00 | Restante: R$0.00", color=ft.colors.GREEN_400, weight=ft.FontWeight.BOLD, size=17)
    
    lista_produtos = ft.Column(scroll="auto", expand=True)

    # --- MONTAGEM DA TELA ---
    page.add(
        lbl_titulo,
        lbl_data,
        ft.Divider(height=10, color="transparent"),
        ent_limite,
        ent_produto,
        linha_preco_qtd,
        ft.Row([btn_add]),
        ft.Divider(height=20),
        lbl_status,
        lista_produtos
    )

# Executa o aplicativo
ft.app(target=main)