import os
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

try:
    from jnius import autoclass  # type: ignore
except ImportError:
    autoclass = None

Window.softinput_mode = "below_target"


# Ajuste visual padrão do fundo
Window.clearcolor = (0.4, 0.4, 0.5, 1)


class CalculadoraKivyFinal(App):
    def build(self):
        self.title = "Calculadora de Compras"
        self.limite = 0.0
        self.total_gasto = 0.0
        self.produtos = []
        self.caminho_ultimo_arquivo = ""
        self.item_selecionado = None

        # Container Principal
        root = BoxLayout(
            orientation="vertical",
            padding=[dp(12), dp(5), dp(12), dp(5)],
            spacing=dp(6),
        )

        # 1. TÍTULO E DATA
        btn_titulo = Button(
            text="CALCULADORA DE COMPRAS",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.17, 0.17, 0.18, 1),
            bold=True,
            font_size="15sp",
        )
        root.add_widget(btn_titulo)

        data_str = datetime.now().strftime("%d/%m/%Y - %H:%M")
        self.lbl_data = Label(
            text=f"Data: {data_str}",
            size_hint_y=None,
            height=dp(20),
            color=(1, 0.65, 1, 1),
            font_size="12sp",
        )
        root.add_widget(self.lbl_data)

        # 2. FORMULÁRIO
        grid_form = GridLayout(cols=2, spacing=dp(6), size_hint_y=None)
        grid_form.bind(minimum_height=grid_form.setter("height"))

        kw_input = {
            "background_color": (0.11, 0.11, 0.12, 1),
            "foreground_color": (1, 1, 1, 1),
            "cursor_color": (0, 1, 1, 1),
            "multiline": False,
            "size_hint_y": None,
            "height": dp(42),
            "write_tab": False,
            "input_type": "text",
        }

        # Linha 1: Disponível
        lbl1 = Label(
            text="Disponível R$:",
            bold=True,
            size_hint=(0.38, None),
            height=dp(42),
            halign="left",
            valign="middle",
        )
        lbl1.bind(size=lbl1.setter("text_size"))
        self.ent_limite = TextInput(
            input_filter="float", size_hint=(0.62, None), **kw_input
        )
        grid_form.add_widget(lbl1)
        grid_form.add_widget(self.ent_limite)

        # Linha 2: Produto
        lbl2 = Label(
            text="Produto:",
            bold=True,
            size_hint=(0.38, None),
            height=dp(42),
            halign="left",
            valign="middle",
        )
        lbl2.bind(size=lbl2.setter("text_size"))
        self.ent_produto = TextInput(size_hint=(0.62, None), **kw_input)
        grid_form.add_widget(lbl2)
        grid_form.add_widget(self.ent_produto)

        # Linha 3: Preço e Quantidade
        lbl3 = Label(
            text="Preço R$:",
            bold=True,
            size_hint=(0.38, None),
            height=dp(42),
            halign="left",
            valign="middle",
        )
        lbl3.bind(size=lbl3.setter("text_size"))

        box_pq = BoxLayout(
            orientation="horizontal",
            spacing=dp(4),
            size_hint=(0.62, None),
            height=dp(42),
        )
        self.ent_preco = TextInput(input_filter="float", size_hint=(0.5, 1), **kw_input)
        lbl_qt = Label(
            text="QT:",
            bold=True,
            size_hint=(0.2, 1),
            halign="center",
            valign="middle",
        )
        lbl_qt.bind(size=lbl_qt.setter("text_size"))
        self.ent_qtd = TextInput(
            text="  1", input_filter="int", size_hint=(0.3, 1), **kw_input
        )

        box_pq.add_widget(self.ent_preco)
        box_pq.add_widget(lbl_qt)
        box_pq.add_widget(self.ent_qtd)

        grid_form.add_widget(lbl3)
        grid_form.add_widget(box_pq)

        root.add_widget(grid_form)

        # --- NAVEGAÇÃO SINCRONIZADA COM CLOCK ---
        def trocar_foco(proximo_campo, *args):
            proximo_campo.focus = True
            proximo_campo.show_keyboard()

        def focar_proximo(instancia, proximo_campo):
            instancia.focus = False
            Clock.schedule_once(lambda dt: trocar_foco(proximo_campo), 0.08)

        self.ent_limite.bind(
            on_text_validate=lambda x: focar_proximo(x, self.ent_produto)
        )
        self.ent_produto.bind(
            on_text_validate=lambda x: focar_proximo(x, self.ent_preco)
        )
        self.ent_preco.bind(on_text_validate=lambda x: focar_proximo(x, self.ent_qtd))
        self.ent_qtd.bind(on_text_validate=lambda x: self.adicionar_produto())

        # 3. PAINEL DE BOTÕES
        box_btn = BoxLayout(
            orientation="horizontal",
            spacing=dp(6),
            size_hint_y=None,
            height=dp(28),
        )

        kw_btn = {
            "background_normal": "",
            "background_color": (0.17, 0.17, 0.18, 1),
            "bold": True,
            "font_size": "13sp",
        }

        btn_add = Button(
            text="Adicionar",
            on_press=lambda x: self.adicionar_produto(),
            **kw_btn,
        )
        btn_exc = Button(
            text="Excluir", on_press=lambda x: self.remover_produto(), **kw_btn
        )
        btn_sal = Button(text="Salvar", on_press=lambda x: self.salvar_txt(), **kw_btn)
        self.btn_env = Button(
            text="Enviar",
            on_press=lambda x: self.compartilhar_nota(),
            disabled=True,
            **kw_btn,
        )

        box_btn.add_widget(btn_add)
        box_btn.add_widget(btn_exc)
        box_btn.add_widget(btn_sal)
        box_btn.add_widget(self.btn_env)
        root.add_widget(box_btn)

        # 4. STATUS DA COMPRA
        self.lbl_status = Label(
            text="Total: R$0.00 | Restante: R$0.00",
            size_hint_y=None,
            height=dp(28),
            color=(0.18, 0.82, 0.34, 1),
            bold=True,
            font_size="14sp",
        )
        root.add_widget(self.lbl_status)

        # 5. LISTA DE PRODUTOS
        scroll = ScrollView(size_hint=(1, 0.5))  #
        self.box_lista = BoxLayout(  # BoxLayout para a lista de produtos
            orientation="vertical", spacing=dp(4), size_hint_y=None
        )
        self.box_lista.bind(
            minimum_height=self.box_lista.setter("height")
        )  # habilita o ajuste automático da altura do BoxLayout com base no conteúdo
        # se a altura do BoxLayout for maior que a altura do ScrollView, o conteúdo será rolável.
        from kivy.graphics import Color, Line

        with self.box_lista.canvas.before:
            Color(0, 1, 1, 1)
            self.borda_lista = Line(
                rectangle=(
                    self.box_lista.x,
                    self.box_lista.y,
                    self.box_lista.width,
                    self.box_lista.height,
                ),
                width=dp(1.5),  # define a largura da borda
            )

        def atualizar_borda(instance, value):
            self.borda_lista.rectangle = (
                instance.x,
                instance.y,
                instance.width,
                instance.height,
            )

        self.box_lista.bind(pos=atualizar_borda, size=atualizar_borda)
        scroll.add_widget(self.box_lista)
        root.add_widget(scroll)

        return root

    def mostrar_alerta(self, titulo, mensagem):
        box = BoxLayout(orientation="vertical", padding=dp(6), spacing=dp(6))

        lbl_msg = Label(
            text=mensagem,
            halign="center",
            valign="middle",
            color=(1, 1, 1, 1),
            font_size="16sp",
        )

        def atualizar_texto(instancia, valor):
            instancia.text_size = (valor[0] - dp(6), None)

        lbl_msg.bind(size=atualizar_texto)
        box.add_widget(lbl_msg)

        btn_ok = Button(
            text="OK",
            size_hint_y=None,
            height=dp(40),
            background_normal="",
            background_color=(0.17, 0.17, 0.18, 1),
            bold=True,
        )
        box.add_widget(btn_ok)

        popup = Popup(
            title=titulo,
            content=box,
            size_hint=(0.8, 0.20),
            auto_dismiss=False,
        )
        btn_ok.bind(on_release=popup.dismiss)
        popup.open()

    def atualizar_status(self):
        restante = self.limite - self.total_gasto
        self.lbl_status.text = (
            f"Total: R${self.total_gasto:.2f} | Restante: R${restante:.2f}"
        )

    def selecionar_item(self, btn):
        for child in self.box_lista.children:
            child.background_color = (0.11, 0.11, 0.12, 1)
        btn.background_color = (0.25, 0.25, 0.28, 1)
        self.item_selecionado = btn

    def adicionar_produto(self):
        try:
            if self.limite == 0.0:
                if not self.ent_limite.text:
                    self.mostrar_alerta("Erro", "Digite o valor disponível!")
                    return
                self.limite = float(self.ent_limite.text.replace(",", "."))
                self.ent_limite.disabled = True

            nome = self.ent_produto.text.strip()
            preco = float(self.ent_preco.text.replace(",", "."))
            qtd = int(self.ent_qtd.text) if self.ent_qtd.text else 1
            subtotal = preco * qtd

            if not nome:
                self.mostrar_alerta("Erro", "Digite um produto!")
                return

            if self.total_gasto + subtotal > self.limite:
                self.mostrar_alerta("Erro", "Ultrapassa o limite disponível!")
                return

            self.total_gasto += subtotal
            self.produtos.append((nome, preco, qtd))

            btn_item = Button(
                text=f" {nome}: R${preco:.2f} x {qtd} = R${subtotal:.2f}",
                size_hint_y=None,
                height=dp(38),
                background_color=(0.11, 0.11, 0.12, 1),
                background_normal="",
                color=(1, 1, 1, 1),
                halign="left",
                valign="middle",
            )
            btn_item.bind(size=btn_item.setter("text_size"))
            btn_item.bind(on_press=self.selecionar_item)

            self.box_lista.add_widget(btn_item)

            self.ent_produto.text = ""
            self.ent_preco.text = ""
            self.ent_qtd.text = "1"

            Clock.schedule_once(lambda dt: self._focar_campo(self.ent_produto), 0.08)

            self.atualizar_status()

        except ValueError:
            self.mostrar_alerta("Erro", "Preencha os campos corretamente!")

    def _focar_campo(self, campo):
        campo.focus = True
        campo.show_keyboard()

    def remover_produto(self):
        if not self.item_selecionado:
            self.mostrar_alerta("Aviso", "Selecione um item da lista para excluir!")
            return

        idx = self.box_lista.children.index(self.item_selecionado)
        idx_real = len(self.produtos) - 1 - idx

        prod_removido = self.produtos.pop(idx_real)
        self.total_gasto -= prod_removido[1] * prod_removido[2]

        self.box_lista.remove_widget(self.item_selecionado)
        self.item_selecionado = None

        self.atualizar_status()

        if not self.produtos and self.total_gasto == 0.0:
            self.ent_limite.disabled = False
            self.limite = 0.0

    def limpar_tela(self):
        self.limite = 0.0
        self.total_gasto = 0.0
        self.produtos.clear()
        self.box_lista.clear_widgets()

        self.ent_limite.disabled = False
        self.ent_limite.text = ""
        self.ent_produto.text = ""
        self.ent_preco.text = ""
        self.ent_qtd.text = "1"

        self.atualizar_status()
        Clock.schedule_once(lambda dt: self._focar_campo(self.ent_limite), 0.08)

    def salvar_txt(self):
        if not self.produtos:
            self.mostrar_alerta("Aviso", "Nenhum produto na lista!")
            return

        pasta = (
            "/storage/emulated/0/Python/NOTA FISCAL/"
            if os.path.exists("/storage/emulated/0/")
            else os.path.expanduser("~/Área de trabalho/")
        )

        try:
            os.makedirs(pasta, exist_ok=True)
            caminho = os.path.join(pasta, "lista_de_compras.txt")
            produto_caro = max(self.produtos, key=lambda x: x[1])
            data_str = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

            with open(caminho, "w", encoding="utf-8") as f:
                f.write("            NOTA DE COMPRA              \n")
                f.write(f"  Data/Hora: {data_str}\n")
                f.write("========================================\n\n")
                f.write("ITENS COMPRADOS:\n")
                f.write("----------------------------------------\n")
                for p, pr, q in self.produtos:
                    f.write(f"{p[:12]:<12} R${pr:>5.2f} x {q:<2} = R${pr*q:>6.2f}\n")
                f.write("----------------------------------------\n")
                f.write(f"TOTAL GASTO:             R${self.total_gasto:>8.2f}\n")
                f.write(f"VALOR DISPONÍVEL:        R${self.limite:>8.2f}\n")
                f.write(
                    f"SALDO RESTANTE:          R${self.limite - self.total_gasto:>8.2f}\n"
                )
                f.write("----------------------------------------\n")
                f.write(
                    f"PRODUTO MAIS CARO: {produto_caro[0]} (R${produto_caro[1]:.2f})\n"
                )
                f.write("========================================\n")

            self.caminho_ultimo_arquivo = caminho
            self.btn_env.disabled = False
            self.mostrar_alerta("Sucesso", "Nota salva")
            self.limpar_tela()

        except Exception as e:
            self.mostrar_alerta("Erro", f"Erro ao salvar: {e}")

    def compartilhar_nota(self):
        if not self.caminho_ultimo_arquivo or not os.path.exists(
            self.caminho_ultimo_arquivo
        ):
            self.mostrar_alerta("Erro", "Arquivo não encontrado!")
            return

        try:
            with open(self.caminho_ultimo_arquivo, "r", encoding="utf-8") as file:
                conteudo = file.read()

            if autoclass is None:
                self.mostrar_alerta(
                    "Info",
                    "Compartilhamento via Android disponível apenas no ambiente Android.",
                )
                return

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")
            String = autoclass("java.lang.String")

            intent = Intent(Intent.ACTION_SEND)
            intent.setType("text/plain")
            intent.putExtra(Intent.EXTRA_TEXT, String(conteudo))
            chooser = Intent.createChooser(intent, String("Enviar Nota de Compra"))
            PythonActivity.mActivity.startActivity(chooser)
        except Exception:
            self.mostrar_alerta(
                "Info",
                f"Função de envio via Android.\nCaminho: {self.caminho_ultimo_arquivo}",
            )


if __name__ == "__main__":
    CalculadoraKivyFinal().run()
