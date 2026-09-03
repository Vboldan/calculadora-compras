import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox


# --- CLASSE PARA CRIAR BOTÃO ARREDONDADO ESTILO TECLADO ---
class BotaoArredondado(tk.Canvas):
    def __init__(
        self,
        parent,
        text,
        command=None,
        bg="#2d2d30",
        fg="#030303",
        radius=22,
        height=58,
        font=("Arial", 8, "normal"),
        **kwargs,
    ):
        super().__init__(
            parent,
            bg=parent["bg"],
            highlightthickness=0,
            bd=0,
            height=height,
            **kwargs,
        )
        self.command = command
        self.bg_color = bg
        self.fg_color = fg
        self.radius = radius
        self.text = text
        self.font = font
        self.estado = "normal"

        self.bind("<Configure>", self._desenhar)
        self.bind("<Button-1>", self._ao_clicar)

    def _desenhar(self, event=None):
        del event
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        r = self.radius

        if w <= 0 or h <= 0:
            return

        self.create_arc(
            0,
            0,
            2 * r,
            2 * r,
            start=90,
            extent=90,
            fill=self.bg_color,
            outline="",
        )
        self.create_arc(
            w - 2 * r,
            0,
            w,
            2 * r,
            start=0,
            extent=90,
            fill=self.bg_color,
            outline="",
        )
        self.create_arc(
            0,
            h - 2 * r,
            2 * r,
            h,
            start=180,
            extent=90,
            fill=self.bg_color,
            outline="",
        )
        self.create_arc(
            w - 2 * r,
            h - 2 * r,
            w,
            h,
            start=270,
            extent=90,
            fill=self.bg_color,
            outline="",
        )

        self.create_rectangle(r, 0, w - r, h, fill=self.bg_color, outline="")
        self.create_rectangle(0, r, w, h - r, fill=self.bg_color, outline="")

        cor_texto = self.fg_color if self.estado == "normal" else "#666666"
        self.create_text(w / 2, h / 2, text=self.text, fill=cor_texto, font=self.font)

    def _ao_clicar(self, event):
        del event
        if self.estado == "normal" and self.command:
            self.command()

    def set_state(self, state):
        self.estado = state
        self._desenhar()


class CalculadoraComprasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Compras")
        self.root.geometry("400x680")

        # --- CORES (TEMA ESCURO) ---
        self.COR_FUNDO = "#404040"
        self.COR_CARD = "#0c1c1e"
        self.COR_BOTAO = "#2c2c6e"
        self.COR_DESTAQUE = "#0a84ff"
        self.COR_EXCLUIR = "#ff453a"
        self.COR_SALVAR = "#30d158"
        self.COR_ENVIAR = "#bf5af2"
        self.COR_TEXTO = "#2fffff"
        self.COR_SUBTEXTO = "#8e8e93"

        self.root.configure(bg=self.COR_FUNDO)

        self.limite = 0.0
        self.total_gasto = 0.0
        self.produtos = []
        self.caminho_ultimo_arquivo = ""

        # --- TÍTULO E DATA ---
        self.card_titulo = BotaoArredondado(
            root,
            text="CALCULADORA DE COMPRAS",
            bg=self.COR_BOTAO,
            fg=self.COR_TEXTO,
            height=100,
            radius=40,
            font=("Arial", 10, "normal"),
        )
        self.card_titulo.pack(fill=tk.X, padx=15, pady=(10, 5))

        data_hora_atual = datetime.now().strftime("%d/%m/%Y - %H:%M")
        self.lbl_data = tk.Label(
            root,
            text=f"Data: {data_hora_atual}",
            font=("Arial", 8),
            bg=self.COR_FUNDO,
            fg=self.COR_SUBTEXTO,
        )
        self.lbl_data.pack(pady=(0, 8))

        # --- FORMULÁRIO COMPACTO ---
        frame_form = tk.Frame(root, bg=self.COR_FUNDO)
        frame_form.pack(fill=tk.X, padx=15, pady=2)

        FONTE_ROTULOS = ("Arial", 10, "normal")

        lbl_limite = tk.Label(
            frame_form,
            text="Disponível R$:",
            bg=self.COR_FUNDO,
            fg=self.COR_TEXTO,
            font=FONTE_ROTULOS,
            anchor="w",
        )
        lbl_limite.grid(row=0, column=0, sticky="w", pady=8)

        self.ent_limite = tk.Entry(
            frame_form,
            font=("Arial", 10),
            bg=self.COR_CARD,
            fg=self.COR_TEXTO,
            insertbackground="white",
            bd=0,
            relief="flat",
            highlightthickness=0,
        )
        self.ent_limite.grid(
            row=0, column=1, columnspan=6, sticky="ew", ipady=4, padx=(5, 0)
        )

        lbl_produto = tk.Label(
            frame_form,
            text="Produto:",
            bg=self.COR_FUNDO,
            fg=self.COR_TEXTO,
            font=FONTE_ROTULOS,
            anchor="w",
        )
        lbl_produto.grid(row=1, column=0, sticky="w", pady=8)

        self.ent_produto = tk.Entry(
            frame_form,
            font=("Arial", 10),
            bg=self.COR_CARD,
            fg=self.COR_TEXTO,
            insertbackground="white",
            bd=0,
            relief="flat",
            highlightthickness=0,
        )
        self.ent_produto.grid(
            row=1, column=1, columnspan=3, sticky="ew", ipady=4, padx=(5, 0)
        )

        lbl_preco = tk.Label(
            frame_form,
            text="Preço R$:",
            bg=self.COR_FUNDO,
            fg=self.COR_TEXTO,
            font=FONTE_ROTULOS,
            anchor="w",
        )
        lbl_preco.grid(row=2, column=0, sticky="w", pady=8)

        self.ent_preco = tk.Entry(
            frame_form,
            font=("Arial", 10),
            bg=self.COR_CARD,
            fg=self.COR_TEXTO,
            insertbackground="white",
            bd=0,
            relief="flat",
            highlightthickness=0,
            width=8,
        )
        self.ent_preco.grid(row=2, column=1, sticky="ew", ipady=8, padx=(5, 5))

        lbl_qtd = tk.Label(
            frame_form,
            text="QT:",
            bg=self.COR_FUNDO,
            fg=self.COR_TEXTO,
            font=FONTE_ROTULOS,
        )
        lbl_qtd.grid(row=2, column=2, sticky="e", padx=(5, 2))

        self.ent_qtd = tk.Entry(
            frame_form,
            font=("Arial", 10),
            bg=self.COR_CARD,
            fg=self.COR_TEXTO,
            insertbackground="white",
            bd=0,
            relief="flat",
            highlightthickness=0,
            width=4,
        )
        self.ent_qtd.grid(row=2, column=3, sticky="ew", ipady=8)
        self.ent_qtd.insert(0, "1")

        frame_form.columnconfigure(1, weight=3)
        frame_form.columnconfigure(3, weight=1)

        # --- NAVEGAÇÃO VIA TECLA ENTER ---
        self.ent_limite.bind("<Return>", lambda e: self.ent_produto.focus_set())
        self.ent_produto.bind("<Return>", lambda e: self.ent_preco.focus_set())
        self.ent_preco.bind("<Return>", lambda e: self.ent_qtd.focus_set())
        self.ent_qtd.bind("<Return>", lambda e: self.adicionar_produto())

        # --- PAINEL DE BOTÕES ---
        frame_botoes = tk.Frame(root, bg=self.COR_FUNDO)
        frame_botoes.pack(fill=tk.X, padx=10, pady=12)

        for col in range(4):
            frame_botoes.columnconfigure(col, weight=1, uniform="grupo_botoes")

        btn_add = BotaoArredondado(
            frame_botoes,
            text="Adicionar",
            command=self.adicionar_produto,
            bg=self.COR_DESTAQUE,
            height=78,
        )
        btn_add.grid(row=0, column=0, padx=3, sticky="ew")

        btn_exc = BotaoArredondado(
            frame_botoes,
            text="Excluir",
            command=self.remover_produto,
            bg=self.COR_EXCLUIR,
            height=78,
        )
        btn_exc.grid(row=0, column=1, padx=3, sticky="ew")

        btn_sal = BotaoArredondado(
            frame_botoes,
            text="Salvar",
            command=self.salvar_txt,
            bg=self.COR_SALVAR,
            height=78,
        )
        btn_sal.grid(row=0, column=2, padx=3, sticky="ew")

        self.btn_compartilhar = BotaoArredondado(
            frame_botoes,
            text="Enviar",
            command=self.compartilhar_nota,
            bg=self.COR_ENVIAR,
            height=78,
        )
        self.btn_compartilhar.grid(row=0, column=3, padx=3, sticky="ew")
        self.btn_compartilhar.set_state("disabled")

        # --- STATUS DA COMPRA ---
        self.lbl_status = tk.Label(
            root,
            text="Total: R$0.00 | Restante: R$0.00",
            bg=self.COR_FUNDO,
            fg="#30d158",
            font=("Arial", 10, "normal"),
        )
        self.lbl_status.pack(pady=4)

        # --- LISTA COM BARRA DE ROLAGEM E ALTURA MANIPULÁVEL ---
        frame_lista = tk.Frame(root, bg=self.COR_FUNDO)
        frame_lista.pack(fill=tk.X, padx=10, pady=(1, 10))  # Alterado para fill=tk.X
        frame_lista.config(
            height=280
        )  # <-- ALTERE ESTE VALOR PARA MANIPULAR O TAMANHO DA CAIXA
        frame_lista.pack_propagate(False)

        self.scrollbar = tk.Scrollbar(
            frame_lista,
            orient=tk.VERTICAL,
            bg=self.COR_CARD,
            troughcolor=self.COR_FUNDO,
            bd=1,
            highlightthickness=0,
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            frame_lista,
            font=("Arial", 10),
            bg=self.COR_CARD,
            fg=self.COR_TEXTO,
            selectbackground="#3a3a3c",  # cor de fundo do item selecionado
            selectforeground="#f10505",  # cor do texto do item selecionado
            bd=0,
            relief="flat",
            highlightthickness=0,
            yscrollcommand=self.scrollbar.set,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        # Força o foco e abre o teclado virtual logo após a janela carregar
        self.root.after(
            100,
            lambda: [
                self.ent_limite.focus_set(),
                # Opcional para alguns ambientes mobile que aceitam evento de clique forçado
                self.ent_limite.event_generate("<Button-1>"),
            ],
        )

    def adicionar_produto(self):
        try:
            if self.limite == 0.0:
                self.limite = float(self.ent_limite.get().replace(",", "."))
                self.ent_limite.config(state="disabled")

            nome = self.ent_produto.get().strip()
            preco = float(self.ent_preco.get().replace(",", "."))
            qtd = int(self.ent_qtd.get())
            subtotal = preco * qtd

            if not nome:
                messagebox.showerror("Erro", "Digite o nome do produto!")
                return

            if self.total_gasto + subtotal > self.limite:
                messagebox.showerror("Erro", "Ultrapassa o limite disponível!")
                return

            self.total_gasto += subtotal
            nome = nome[:20]  # Limita o nome a 20 caracteres
            traços = "-" * (20 - len(nome))  # Calcula a quantidade de traços
            nome_formatado = f"{nome}{traços}"  # Formata o nome com traços
            self.produtos.append((nome_formatado, preco, qtd))
            self.listbox.insert(
                tk.END, f" {nome_formatado }: R${preco:.2f} x {qtd} = R${subtotal:.2f}"
            )

            self.ent_produto.delete(0, tk.END)
            self.ent_preco.delete(0, tk.END)
            self.ent_qtd.delete(0, tk.END)
            self.ent_qtd.insert(0, "1")
            self.ent_produto.focus_set()

            self.atualizar_status()

        except ValueError:
            messagebox.showerror("Erro", "Preencha os campos corretamente!")

    def remover_produto(self):
        try:
            indice = self.listbox.curselection()[0]
            prod_removido = self.produtos.pop(indice)

            subtotal_removido = prod_removido[1] * prod_removido[2]
            self.total_gasto -= subtotal_removido

            self.listbox.delete(indice)
            self.atualizar_status()

            if not self.produtos and self.total_gasto == 0.0:
                self.ent_limite.config(state="normal")
                self.limite = 0.0

        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um item na lista para remover!")

    def limpar_tela(self):
        self.limite = 0.0
        self.total_gasto = 0.0
        self.produtos.clear()

        self.listbox.delete(0, tk.END)

        self.ent_limite.config(state="normal")
        self.ent_limite.delete(0, tk.END)
        self.ent_produto.delete(0, tk.END)
        self.ent_preco.delete(0, tk.END)
        self.ent_qtd.delete(0, tk.END)
        self.ent_qtd.insert(0, "1")

        self.atualizar_status()

    def atualizar_status(self):
        restante = self.limite - self.total_gasto
        self.lbl_status.config(
            text=f"Total: R${self.total_gasto:.2f} | Restante: R${restante:.2f}"
        )

    def salvar_txt(self):
        if not self.produtos:
            messagebox.showwarning("Aviso", "Nenhum produto na lista!")
            return

        if os.path.exists("/storage/emulated/0/"):
            pasta = "/storage/emulated/0/Python/NOTA FISCAL/"
        else:
            pasta = os.path.expanduser("~/Área de trabalho/")

        try:
            os.makedirs(pasta, exist_ok=True)
            caminho = os.path.join(pasta, "lista_de_compras.txt")

            produto_caro = max(self.produtos, key=lambda x: x[1])
            data_str = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

            with open(caminho, "w", encoding="utf-8") as f:
                f.write("========================================\n")
                f.write("            NOTA DE COMPRA              \n")
                f.write(f"  Data/Hora: {data_str}\n")
                f.write("========================================\n\n")

                f.write("ITENS COMPRADOS:\n")
                f.write("----------------------------------------\n")
                for p, pr, q in self.produtos:
                    nome_formatado = p[:12]
                    f.write(
                        f"{nome_formatado:<12} R${pr:>5.2f} x {q:<2} = R${pr*q:>6.2f}\n"
                    )

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
            self.btn_compartilhar.set_state("normal")

            messagebox.showinfo(
                "Sucesso",
                f"Nota salva com sucesso!\nCaminho: {caminho}",
            )
            self.limpar_tela()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    def compartilhar_nota(self):
        if not self.caminho_ultimo_arquivo or not os.path.exists(
            self.caminho_ultimo_arquivo
        ):
            messagebox.showerror("Erro", "Arquivo de nota não encontrado!")
            return

        try:
            with open(self.caminho_ultimo_arquivo, "r", encoding="utf-8") as file:
                conteudo = file.read()

            autoclass = __import__("jnius", fromlist=["autoclass"]).autoclass

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")
            String = autoclass("java.lang.String")

            intent = Intent(Intent.ACTION_SEND)
            intent.setType("text/plain")
            intent.putExtra(Intent.EXTRA_TEXT, String(conteudo))

            chooser = Intent.createChooser(intent, String("Enviar Nota de Compra"))
            PythonActivity.mActivity.startActivity(chooser)

        except (ModuleNotFoundError, ImportError):
            messagebox.showinfo(
                "Info (Linux)",
                f"A função de enviar via Android só funciona no celular.\n\nArquivo gerado em:\n{self.caminho_ultimo_arquivo}",
            )
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível compartilhar: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraComprasApp(root)
    root.mainloop()
