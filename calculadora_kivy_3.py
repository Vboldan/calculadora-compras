import os # Importa a biblioteca para interagir com o sistema operacional (pastas e arquivos)
from datetime import datetime # Importa a ferramenta para trabalhar com dados de data e hora

try: # Inicia um bloco de tratamento de exceções (para evitar que o app quebre se faltar algo)
    from Fjnius import autoclass # Tenta importar a ferramenta para usar recursos nativos do Android
except ( # Captura exceções caso o código não esteja rodando no celular Android
    ImportError, # Tipo de erro acionado quando a importação falha
    ModuleNotFoundError, # Tipo de erro acionado quando o módulo não é encontrado
):  # jnius existe apenas em ambiente Android/Kivy # Comentário original mantido
    autoclass = None # Define a variável como nula se o jnius não estiver disponível no sistema

from kivy.app import App # Importa a classe principal base para criar o aplicativo Kivy
from kivy.clock import Clock # Importa o relógio interno para agendar o tempo das funções
from kivy.core.window import Window # Importa a janela principal do aplicativo
from kivy.metrics import dp # Importa o medidor de pixels independentes de densidade de tela
from kivy.uix.boxlayout import BoxLayout # Importa o organizador de layout de caixas (horizontal/vertical)
from kivy.uix.button import Button # Importa o elemento visual para criar botões clicáveis
from kivy.uix.gridlayout import GridLayout # Importa o organizador de layout em formato de grade
from kivy.uix.label import Label # Importa o elemento de texto estático (rótulo descritivo)
from kivy.uix.popup import Popup # Importa a estrutura de janela flutuante de alerta
from kivy.uix.scrollview import ScrollView # Importa a estrutura para criar uma visualização com barra de rolagem
from kivy.uix.textinput import TextInput # Importa o campo retangular de entrada de texto para digitação

Window.softinput_mode = "below_target" # Configura o teclado do celular para subir a tela e não cobrir o texto
Window.clearcolor = (0.6, 0.4, 0.5, 1) # Define a cor de fundo padrão da janela principal do aplicativo


class CalculadoraKivyFinal(App): # Cria a classe principal do aplicativo herdando a estrutura do App do Kivy
    # Paleta de cores centralizada para facilitar a manipulação futura # Comentário original mantido
    CORES_BOTOES = { # Cria um dicionário de dados para armazenar os códigos das cores dos botões
        "titulo": (0.17, 0.17, 0.18, 1), # Define a cor cinza-escura do botão de título
        "adicionar": (0.17, 0.17, 0.50, 1), # Define a cor azulada do botão de adicionar
        "excluir": (0.50, 0.17, 0.18, 1), # Define a cor avermelhada do botão de excluir
        "salvar": (0.17, 0.50, 0.18, 1), # Define a cor esverdeada do botão de salvar a nota
        "enviar": (0.50, 0.50, 0.80, 1), # Define a cor roxa clara do botão de envio/compartilhamento
        "popup": (0.17, 0.17, 0.18, 1), # Define a cor escura do botão interno do alerta (popup)
    } # Fecha o dicionário de cores

    def build(self): # Método principal que o Kivy chama para construir e desenhar a interface gráfica
        self.title = "Calculadora de Compras" # Define o título do aplicativo que aparece no sistema
        self.limite = 0.0 # Inicializa a variável financeira do limite orçamentário com valor zero
        self.total_gasto = 0.0 # Inicializa a variável da soma total dos produtos com valor zero
        self.produtos = [] # Cria uma lista vazia que vai guardar os dados dos produtos na memória
        self.caminho_ultimo_arquivo = "" # Cria um texto vazio para depois guardar onde o TXT foi salvo
        self.item_selecionado = None # Inicializa a variável que marcará qual item da lista foi tocado

        root = BoxLayout( # Cria o layout principal, que será a caixa que vai conter tudo dentro
            orientation="vertical", # Define a orientação da caixa mestra como vertical
            padding=[ # Inicia a definição de margens internas nas bordas do layout
                dp(12), # Margem interna no lado esquerdo
                dp(5), # Margem interna no topo
                dp(12), # Margem interna no lado direito
                dp(5), # Margem interna na parte inferior
            ],  # dp(12) esquerda/direita, dp(5) cima/baixo # Comentário original mantido
            spacing=dp(6), # Define um pequeno espaço padrão entre os blocos dentro da caixa principal
        ) # Fecha as propriedades da configuração do layout principal

        # Montagem estruturada da interface # Comentário original mantido
        root.add_widget(self._criar_cabecalho()) # Chama a função do cabeçalho e insere na caixa principal
        root.add_widget(self._criar_formulario()) # Chama a função do formulário e insere logo abaixo
        root.add_widget(self._criar_painel_botoes()) # Chama a função dos botões e insere na tela
        root.add_widget(self._criar_status()) # Chama a função dos totais financeiros e insere
        root.add_widget(self._criar_lista_produtos()) # Chama a área da lista de itens e finaliza a tela
        
        Clock.schedule_once(lambda dt: self._focar_campo(self.ent_limite), 0.05) # Manda focar no campo Limite após abrir o app

        return root # Devolve o layout principal (com todas as peças montadas) para exibição na tela

    def _criar_cabecalho(self): # Declara a função para criar os elementos da parte superior (título e data)
        layout = BoxLayout( # Cria uma mini-caixa exclusiva para organizar o cabeçalho
            orientation="vertical", size_hint_y=None, height=dp(72), spacing=dp(4) # Vertical, altura física travada em 72dp e espaçado
        ) # Fecha a configuração da caixa do cabeçalho

        btn_titulo = Button( # Cria um botão falso apenas para servir de título estilizado
            text="CALCULADORA DE COMPRAS", # Define o texto exibido
            size_hint_y=None, # Desativa o redimensionamento elástico de altura
            height=dp(48), # Crava a altura do botão do título em 48dp
            background_normal="", # Remove o sombreado padrão do Kivy para cores ficarem sólidas
            background_color=self.CORES_BOTOES["titulo"], # Pega a cor correspondente lá no dicionário
            bold=True, # Transforma a fonte em negrito
            font_size="15sp", # Define o tamanho da fonte
        ) # Fecha os atributos do botão de título
        layout.add_widget(btn_titulo) # Adiciona este título dentro do layout do cabeçalho

        data_str = datetime.now().strftime("%d/%m/%Y - %H:%M") # Pega relógio do sistema e formata (Dia/Mês/Ano - Hora:Min)
        self.lbl_data = Label( # Cria o texto simples para exibir a hora
            text=f"Data: {data_str}", # Injeta a hora formatada no texto
            size_hint_y=None, # Impede de esticar a altura
            height=dp(20), # Define a altura do texto da data
            color=(1, 0.65, 1, 1), # Define um tom de rosa claro para o texto
            font_size="12sp", # Define a fonte da data ligeiramente menor
        ) # Fecha a criação do rótulo da data
        layout.add_widget(self.lbl_data) # Adiciona a data abaixo do título
        return layout # Devolve a mini-caixa pronta com o cabeçalho

    def _criar_formulario(self): # Declara a função que gera toda a área de digitação (Limite, Produto, Valor)
        grid_form = GridLayout(cols=2, spacing=dp(6), size_hint_y=None) # Cria layout de grade com 2 colunas lado a lado
        grid_form.bind(minimum_height=grid_form.setter("height")) # Faz a grade de fundo crescer o necessário para caber o texto

        kw_input = { # Cria um dicionário para configurar os campos de texto padronizados sem repetir código
            "background_color": (0.11, 0.11, 0.12, 1),  # Fundo escuro para contraste # Cor interna do campo de digitação
            "foreground_color": ( # Inicia o parêntese para definir a cor da fonte digitada
                1, # Quantidade de Vermelho (máximo)
                1, # Quantidade de Verde (máximo)
                1, # Quantidade de Azul (máximo)
                1, # Nível de opacidade (sólido) - Juntos formam a cor branca
            ),  # Cor do texto branca para melhor visibilidade # Comentário original
            "cursor_color": (0, 1, 1, 1),  # Cor do cursor em ciano para destaque # Define o traço piscante na cor ciano
            "multiline": False,  # Permitir apenas uma linha de entrada # Impede de pular linha ao apertar Enter
            "size_hint_y": None,  # Não definir altura automaticamente # Trava a altura dinâmica
            "height": dp(32),  # Altura fixa para os campos de entrada # Determina a grossura do campo visual
            "write_tab": False,  # Desativar o tab para escrita # Evita digitar um tab invisível no campo
            "input_type": "text",  # Tipo de entrada como texto para flexibilidade # Ativa o teclado geral (padrão)
        } # Finaliza o dicionário de padronização

        def criar_campo(texto_lbl, eh_float=False, eh_qtd=False): # Função embutida rápida para criar a dupla Rótulo+Campo
            lbl = Label( # Cria o texto descritivo lateral
                text=texto_lbl, # Recebe o texto que foi pedido ao chamar
                #bold=True, # (Comentado) deixaria o texto negrito, mas está desativado
                size_hint=(0.38, None), # Dá 38% do espaço da linha para o texto e desativa a altura flexível
                height=dp(42), # Altura do texto alinhado com o campo
                halign="left", # Empurra o alinhamento de texto para a borda esquerda
                valign="middle", # Mantém o texto no centro da linha verticalmente
            ) # Fecha o texto descritivo
            lbl.bind(size=lbl.setter("text_size")) # Truque do Kivy que obriga o alinhamento a respeitar as bordas da tela

            if eh_qtd: # Testa se quem chamou a função pediu especificamente o campo de quantidade
                campo = TextInput( # Se sim, cria o campo de texto configurado para a Quantidade
                    text=" 1", input_filter="int", size_hint=(0.3, 1), **kw_input # Pré-preenche "1", filtra só inteiros, ocupa 30% da linha
                )  # Campo de quantidade com filtro para inteiros # Comentário original mantido
            else: # Se não for o campo quantidade (ex: limite, produto, preço)
                filtro = ( # Define qual será o comportamento das teclas de números
                    "float" if eh_float else None # Ativa números quebrados/decimais se pediu "eh_float", senão aceita letras
                )  # Campo de preço com filtro para números decimais, caso seja necessário # Comentário original mantido
                campo = TextInput( # Cria o campo de texto padrão do formulário
                    input_filter=filtro, size_hint=(0.62, None), **kw_input # Aplica o filtro calculado e dá 62% da largura
                ) # Encerra o campo
            return lbl, campo # Retorna o conjunto montadinho (Texto Descritivo + Campo em Branco)

        lbl1, self.ent_limite = criar_campo("Disponível R$:", eh_float=True) # Chama o criador para montar a área de orçamentos decimais
        lbl2, self.ent_produto = criar_campo("Produto:") # Chama o criador para montar a área de nome de produto (letras)

        grid_form.add_widget(lbl1) # Posiciona o texto do orçamento na primeira célula da grade
        grid_form.add_widget(self.ent_limite) # Posiciona o campo na segunda célula da grade
        grid_form.add_widget(lbl2) # Posiciona o texto do produto abaixo
        grid_form.add_widget(self.ent_produto) # Posiciona o campo de produto na frente

        # Preço e Quantidade combinados # Comentário original mantido
        lbl3, self.ent_preco = criar_campo("Preço R$:", eh_float=True) # Cria o campo e o texto de preço
        box_pq = BoxLayout( # Cria uma sub-caixa horizontal para aninhar Preço e Quantidade na mesma linha
            orientation="horizontal", # Deixa tudo lado a lado
            spacing=dp(4), # Espaçamento curto entre Preço e Quantidade
            size_hint=(0.62, None), # A caixa inteira ocupa 62% do espaço restante da grade
            height=dp(42), # Altura idêntica à do texto principal
        ) # Fim da criação da caixa embutida

        self.ent_preco.size_hint_x = 0.5 # Força o campo de Preço a ocupar metade dessa sub-caixa
        lbl_qt = Label( # Cria um micro-texto "QT" para ficar entre preço e quantidade
            text="QT:", bold=True, size_hint=(0.2, 1), halign="center", valign="middle" # Ocupa 20%, negrito e centralizado
        ) # Fim do texto QT
        lbl_qt.bind(size=lbl_qt.setter("text_size")) # Regra padrão de alinhamento visual do Kivy
        _, self.ent_qtd = criar_campo("", eh_qtd=True) # Cria o campo quantidade ignorando o rótulo ("_") porque já fizemos o QT acima

        box_pq.add_widget(self.ent_preco) # Coloca o campo preço na sub-caixa horizontal
        box_pq.add_widget(lbl_qt) # Coloca a palavra QT na sub-caixa horizontal
        box_pq.add_widget(self.ent_qtd) # Coloca o campo de digitar quantidade na sub-caixa

        grid_form.add_widget(lbl3) # Adiciona o texto "Preço R$:" na coluna 1 da grade principal
        grid_form.add_widget(box_pq) # Adiciona a sub-caixa embutida (Preço+QT+Quantidade) na coluna 2

        # Navegação por Enter # Comentário original mantido
        self.ent_limite.bind( # Liga a tecla de conclusão do teclado no celular
            on_text_validate=lambda x: self._focar_proximo(x, self.ent_produto) # Dispara a função para pular ao campo de Produto
        ) # Fecha associação
        self.ent_produto.bind( # Liga o Enter no campo Produto
            on_text_validate=lambda x: self._focar_proximo(x, self.ent_preco) # Pula para o Preço
        ) # Fecha associação
        self.ent_preco.bind( # Liga o Enter no campo de Preço
            on_text_validate=lambda x: self._focar_proximo(x, self.ent_qtd) # Pula para Quantidade
        ) # Fecha associação
        self.ent_qtd.bind(on_text_validate=lambda x: self.adicionar_produto()) # O Enter final da Quantidade dispara a inserção na lista

        return grid_form # Devolve todo o formulário perfeitamente formatado para o aplicativo principal

    def _focar_proximo(self, instancia, proximo_campo): # Função que lida com a transição do cursor (teclado piscando)
        instancia.focus = False # Desliga o foco do campo atual
        Clock.schedule_once(lambda dt: self._focar_campo(proximo_campo), 0.03) # Agenda o próximo campo sem atrasar o teclado

    def _criar_painel_botoes(self): # Declara a função para a faixa de ações centrais
        box_btn = BoxLayout( # Cria o bloco contenedor horizontal
            orientation="horizontal", spacing=dp(6), size_hint_y=None, height=dp(28) # Lado a lado, espaçado, altura fina
        ) # Fecha configuração do container

        kw_btn = {"background_normal": "", "bold": True, "font_size": "13sp"} # Variável padronizada para encurtar formatações de botões

        btn_add = Button( # Cria botão
            text="Adicionar", # Palavra escrita
            background_color=self.CORES_BOTOES["adicionar"], # Pega cor
            on_press=lambda x: self.adicionar_produto(), # Função executada no clique
            **kw_btn, # Aplica estilos padrão do botão visual
        ) # Encerra botão de adição
        btn_exc = Button( # Cria botão
            text="Excluir", # Palavra escrita
            background_color=self.CORES_BOTOES["excluir"], # Pega cor
            on_press=lambda x: self.remover_produto(), # Chama deleção de item selecionado
            **kw_btn, # Estilos padrão
        ) # Encerra botão de exclusão
        btn_sal = Button( # Cria botão
            text="Salvar", # Palavra escrita
            background_color=self.CORES_BOTOES["salvar"], # Pega cor
            on_press=lambda x: self.salvar_txt(), # Chama função de criar nota fiscal
            **kw_btn, # Estilos padrão
        ) # Encerra botão de salvar
        self.btn_env = Button( # Cria botão guardando na própria classe (para ativá-lo depois de salvar)
            text="Enviar", # Palavra
            background_color=self.CORES_BOTOES["enviar"], # Cor
            on_press=lambda x: self.compartilhar_nota(), # Dispara compartilhamento do Android (WhatsApp)
            disabled=True, # Começa travado e esbranquiçado
            **kw_btn, # Estilos padrão
        ) # Encerra botão de envio

        for b in [btn_add, btn_exc, btn_sal, self.btn_env]: # Laço rápido de repetição
            box_btn.add_widget(b) # Joga cada um dos 4 botões pra dentro da faixa horizontal
        return box_btn # Devolve painel montado

    def _criar_status(self): # Declara criador da barra de informações financeiras
        self.lbl_status = Label( # Monta texto
            text="Total: R$0.00 | Restante: R$0.00", # Define estado zerado inicial
            size_hint_y=None, # Barra altura automática
            height=dp(28), # Crava tamanho vertical
            color=(0.18, 0.82, 0.34, 1), # Cor verde vivo para remeter a dinheiro
            bold=True, # Negritado
            font_size="14sp", # Fonte tamanho 14
        ) # Encerra montagem do Label
        return self.lbl_status # Entrega ao app
    
    def _criar_lista_produtos(self): # Declara a área inferior de resultados (onde estava o erro na sua versão)
        # A IDENTAÇÃO FOI CORRIGIDA ABAIXO, ALINHANDO TODAS AS VARIÁVEIS PARA DENTRO DESTE BLOCO! # Comentário explicativo 
        # 1. Cria um container principal para organizar a tela de cima a baixo # Comentário original mantido
        layout_principal = BoxLayout(orientation="vertical", spacing=dp(4)) # Container para lista e footer

        # 2. O ScrollView da lista de produtos agora ocupa o espaço flexível (size_hint_y=1) # Comentário original
        scroll = ScrollView( # Elemento mágico do Kivy que gera barra de rolagem quando a tela enche
            size_hint=(1, 1), bar_width=dp(6), scroll_type=["bars", "content"] # Flexível, barra fina, rola arrastando dedo
        ) # Fim do scroll
        
        self.box_lista = BoxLayout( # A caixa real onde as linhas dos produtos ficarão salvas
            orientation="vertical", spacing=dp(4), size_hint_y=None # Crescimento vertical sem limite pré-definido
        ) # Fim da criação da caixa
        self.box_lista.bind(minimum_height=self.box_lista.setter("height")) # Faz a caixa se espichar de acordo com número de itens

        from kivy.graphics import Color, Line # Importa módulos manuais de desenho de interface 

        with self.box_lista.canvas.before: # Entra no modo pincel, desenhando ANTES dos botões (por baixo deles)
            Color(0, 0, 0, 0) # Pinta invisível/fundo transparente
            self.borda_lista = Line( # Desenha a borda visual enquadrando
                rectangle=( # Formato quadro
                    self.box_lista.x, # Origem eixo X
                    self.box_lista.y, # Origem eixo Y
                    self.box_lista.width, # Largura da tela
                    self.box_lista.height, # Altura calculada
                ), # Fim dos vértices
                width=dp(1.4), # Espessura da linha estética
            ) # Fim da criação da borda

        self.box_lista.bind( # Liga eventos para se a pessoa girar a tela, ou preencher a lista
            pos=lambda inst, val: setattr( # Ao detectar mudança de posição...
                self.borda_lista, "rectangle", (inst.x, inst.y, inst.width, inst.height) # Refaz o retângulo
            ), # Fecha regra
            size=lambda inst, val: setattr( # Ao detectar mudança de altura...
                self.borda_lista, "rectangle", (inst.x, inst.y, inst.width, inst.height) # Redesenha a borda espichada
            ), # Fecha regra 2
        ) # Fim do gatilho dinâmico
        
        # (O rótulo foi removido daqui de dentro para não acompanhar a rolagem) # Comentário original mantido

        scroll.add_widget(self.box_lista) # Joga a caixa de lista finita pra dentro do mecanismo gerador de rolagem infinita
        
        # 3. Adiciona o ScrollView no layout principal # Comentário original mantido
        layout_principal.add_widget(scroll) # O layout base ganha o scroll

        # 4. Criamos o rodapé solto, fora da lista, fixo na base da tela # Comentário original mantido
        lbl_rodape = Label( # Texto dos créditos finais da sua autoria
            text="Calculadora de Compras | Desenvolvido por Valdeci Boldan", # Mostra nome do criador
            size_hint_y=None, # Sem variação vertical
            height=dp(25), # Altura pequena
            color=(0, 0, 0, 1), # Tom de cinza para ser discreto
            font_size="11sp", # Letra reduzida
            halign="center", # Centro esquerdo
            valign="middle", # Centro superior
        ) # Fim da etiqueta
        lbl_rodape.bind(size=lbl_rodape.setter("text_size")) # Ajuste mandatório para funcionar o halign/valign perfeitamente
        
        # 5. Adiciona o rodapé diretamente no layout principal (abaixo de tudo) # Comentário original mantido
        layout_principal.add_widget(lbl_rodape) # Insere ele abaixo do scroll limitando sua posição no roda-pé

        return layout_principal # A função finaliza entregando essa parte gigante da UI

    
    def mostrar_alerta(self, titulo, mensagem): # Mecanismo mestre de janelinhas de erro no meio da tela
        box = BoxLayout(orientation="vertical", padding=dp(6), spacing=dp(6)) # Caixa container das informações do aviso
        lbl_msg = Label( # Cria texto da mensagem 
            text=mensagem, # Insere string que recebeu quando foi ativada
            halign="center", # Centralizado
            valign="middle", # Meio
            color=(1, 1, 1, 1), # Branco
            font_size="16sp", # Bem legível
        ) # Fim do label
        lbl_msg.bind( # Liga quebra de linha dinâmica (word wrap)
            size=lambda inst, val: setattr(inst, "text_size", (val[0] - dp(6), None)) # Calcula o tamanho da tela e desconta a margem
        ) # Fim da amarração elástica
        box.add_widget(lbl_msg) # Põe texto do aviso no layout

        btn_ok = Button( # Botão para usuário poder sumir com o popup
            text="OK", # Etiqueta
            size_hint_y=None, # Altura travada
            height=dp(40), # Tamanho robusto pro dedo não errar no touch
            background_normal="", # Design chapado
            background_color=self.CORES_BOTOES["popup"], # Cor acinzentada
            bold=True, # Negrito
        ) # Finaliza design
        box.add_widget(btn_ok) # Coloca na tela do aviso

        popup = Popup( # Invoca a classe nativa de janelas flutuantes Kivy
            title=titulo, content=box, size_hint=(0.8, 0.40), auto_dismiss=False # Título, Conteúdo interno, 80% larg./20% alt., impede tocar fora pra fechar
        ) # Fim da configuração do frame 
        btn_ok.bind(on_release=popup.dismiss) # Se usuário soltar o dedo do botão, dá comando ao popup para desaparecer
        popup.open() # Instância a tela na frente de tudo

    def atualizar_status(self): # Função matemática do roda-pé informativo
        restante = self.limite - self.total_gasto # Subtrai da variável mestra, a quantidade toda já consumida
        self.lbl_status.text = ( # Injeta no texto verde lá do topo
            f"Total: R${self.total_gasto:.2f} | Restante: R${restante:.2f}" # Usando f-strings e formatando ponto flutuante em 2 casas
        ) # Fim

    def selecionar_item(self, btn): # Gatilho para quando a pessoa pressiona o dedo sobre um item já cadastrado
        for child in self.box_lista.children: # Laço de repetição que varre todos os botões que existem na caixa de rolagem
            child.background_color = (0.11, 0.11, 0.12, 1) # Pinta todo mundo da cor de fundo (reseta outras seleções pra desmarcar)
        btn.background_color = (0.25, 0.25, 0.28, 1) # Ilumina suavemente e unicamente o botão onde a pessoa apertou
        self.item_selecionado = btn # Salva esse botão na variável apontadora de exclusão (alvo marcado)

    def adicionar_produto(self): # Motor logico ativado no botão Adicionar (ou Enter final)
        try: # Protege o app de um crash (fechar sozinho) se o usuário colocar letras onde devia ter números
            if self.limite == 0.0: # Regra inicial: se estiver tudo zerado significa que é o 1º item 
                if not self.ent_limite.text: # Se o campo limite também estiver vazio em tela
                    self.mostrar_alerta("Erro", "Digite o valor disponível!") # Chama janela avisando do erro
                    return # Quebra e encerra o código bem aqui para não avariar o resto
                self.limite = float(self.ent_limite.text.replace(",", ".")) # Se tiver limite, ele transforma ( , ) brasileira em ( . ) americano do Python
                self.ent_limite.disabled = True # Apaga a edição do limite pra pessoa não trocar a grana no meio da compra

            nome = self.ent_produto.text.strip() # Armazena o nome e remove espaços inúteis (strip) no inicio e fim
            preco = float(self.ent_preco.text.replace(",", ".")) # Mesma substituição de ponto decimal no campo preço
            qtd = int(self.ent_qtd.text) if self.ent_qtd.text else 1 # Le a Quantidade ou deduz que é 1 (padrão)
            subtotal = preco * qtd # Matemática básica do peso do item no carrinho

            if not nome: # Proteção extra: se estiver sem nome de produto
                self.mostrar_alerta("Erro", "Digite um produto!") # Mostra pop
                return # Aborta procedimento

            if self.total_gasto + subtotal > self.limite: # Bloqueio de Orçamento: se valor atual + esse novo item for maior que a bolsa inteira
                self.mostrar_alerta("Erro", "Ultrapassa o limite disponível!") # Impede compra de acontecer
                return # Aborta procedimento

            self.total_gasto += subtotal # Estando tudo certo, atualiza e incrementa (+=) o acumulado total
            self.produtos.append((nome, preco, qtd)) # Cria uma tupla inalterável com Nome, Preço e Qt. e salva na lista oculta

            btn_item = Button( # Gera a linha do produto clicável de forma visual 
                text=f" {nome}: R${preco:.2f} x {qtd} = R${subtotal:.2f}", # Imprime formatado (Ex: Maça: R$2.00 x 2 = R$4.00)
                size_hint_y=None, # Barra variação elástica
                height=dp(28),        # Altura do botão para melhor visualização # Comentário original mantido
                background_color=(0,0,0,0),    # Fundo transparente para destacar o texto # Comentário original mantido
                background_normal="", # Retira renderização cinza defaut
                color=(1, 1, 1, 1),# Cor do texto branca para contraste # Comentário original mantido
                halign="left", # Texto à esquerda
                valign="middle", # Texto no centro horizontal
            ) # Final da linha
            btn_item.bind(size=btn_item.setter("text_size")) # Ajuste de halign
            btn_item.bind(on_press=self.selecionar_item) # Amarração que diz que quando clicado ele dispara a iluminação e seleção de exclusão 

            self.box_lista.add_widget(btn_item) # Bota a linha nova na tela e lista

            self.ent_produto.text = "" # Esvazia nome pro próximo registro
            self.ent_preco.text = "" # Esvazia campo preço
            self.ent_qtd.text = "1" # Restaura quantidade 1 defaut

            Clock.schedule_once(lambda dt: self._focar_campo(self.ent_produto), 0.03) # Move o teclado do celular de volta pra caixa Nome
            self.atualizar_status() # Roda atualização na barra verde de Dinheiro x Gasto

        except ValueError: # Caso estoure no bloco Try
            self.mostrar_alerta("Erro", "Preencha os campos corretamente!") # Exemplo: botou "10" e "a" onde era grana

    def _focar_campo(self, campo): # Funçao de conveniência focadora
        campo.focus = True # Dá o alvo elétrico da tela
        campo.show_keyboard() # Abre forçado o teclado touch screen

    def remover_produto(self): # Rotina do botão de Excluir 
        if not self.item_selecionado: # Se o cara apertou "Excluir" sem tocar em ninguém
            self.mostrar_alerta("Aviso", "Selecione um item da lista para excluir!") # Barra operação
            return # Interrompe método

        idx = self.box_lista.children.index(self.item_selecionado) # Acha o índice de posição (0, 1, 2) da lista visual tocada
        idx_real = len(self.produtos) - 1 - idx # Como o Kivy inverte as pilhas (novo por cima de velho), inverte na marra a numeração real do Python

        prod_removido = self.produtos.pop(idx_real) # Extrai definitivamente da lista de memória (produtos[]) com o POP, estraindo dados
        self.total_gasto -= prod_removido[1] * prod_removido[2] # Pega o valor 1 e 2 das tuplas internas(preço, quantidade) e desconta da soma

        self.box_lista.remove_widget(self.item_selecionado) # Elimina graficamente o botão colorido da tela pro usuário
        self.item_selecionado = None # Esvazia a seleção pra limpar rastros

        self.atualizar_status() # Conserta painel verde

        if not self.produtos and self.total_gasto == 0.0: # Se deletou todos e esvaziou TUDO
            self.ent_limite.disabled = False # Devolve liberdade de refazer o orçamento
            self.limite = 0.0 # Restaura zero na mente

    def limpar_tela(self): # Rotina que ocorre pós envio/salvamento para iniciar lista 0 KM
        self.limite = 0.0 # Zera variável
        self.total_gasto = 0.0 # Zera Variável
        self.produtos.clear() # Limpa inteira array interno
        self.box_lista.clear_widgets() # Apaga com raio varredor todo conteúdo estético dos produtos

        self.ent_limite.disabled = False # Destrava edição de limite
        self.ent_limite.text = "" # Exclui tela limite
        self.ent_produto.text = "" # Exclui nome visualmente
        self.ent_preco.text = "" # Exclui valor
        self.ent_qtd.text = "1" # Restaura visual

        self.atualizar_status() # Bota rodape pra verde em R$ 0,00
        Clock.schedule_once(lambda dt: self._focar_campo(self.ent_limite), 0.03) # Manda foco pro primeirão!

    def salvar_txt(self): # Rotina ativada no botão de Salvar Nota (Geradora da NFe local)
        if not self.produtos: # Bloqueio de salvamento vazio
            self.mostrar_alerta("Aviso", "Nenhum produto na lista!") # Exibe janela
            return # Aborta processo de I/O em arquivo

        pasta = ( # Escolhe uma pasta que o sistema permita gravar
            self.user_data_dir # No Android, usa o armazenamento privado do aplicativo
            if autoclass is not None # Detecta a execução Android pelo pyjnius
            else os.path.expanduser("~/Área de trabalho/") # No Linux, mantém o arquivo na área de trabalho
        ) # Fim da escolha de pasta

        try: # Proteção de salvamento de arquivo (costuma dar erro de permissão Android)
            os.makedirs(pasta, exist_ok=True) # Cria árvore de pastas a força (ignorando se já houver uma)
            caminho = os.path.join(pasta, "lista_de_compras.txt") # Concatena rota da pasta com nome definitivo do Bloco de Notas
            produto_caro = max(self.produtos, key=lambda x: x[1]) # Extrai uma métrica divertida de quem é o mais caro baseado na posição de index [1] da tupla
            data_str = datetime.now().strftime("%d/%m/%Y - %H:%M:%S") # Prepara tag temporal exata do click em salvar

            with open(caminho, "w", encoding="utf-8") as f: # Abre porta de I/O com instrução de Sobrescrita ("w") usando codificação Brasil(utf8)
                f.write("            NOTA DE COMPRA              \n") # Cria cabeçalho fiscal alinhado e quebra \n
                f.write(f"  Data/Hora: {data_str}\n") # Registra data real extraida no momento
                f.write("========================================\n\n") # Decoração
                f.write("ITENS COMPRADOS:\n") # Subtitulo
                f.write("----------------------------------------\n") # Decoração
                for p, pr, q in self.produtos: # Loop mágico iterando Nome(p), Preço(pr) e Qtd(q) em todos da tupla
                    f.write(f"{p[:12]:<12} R${pr:>5.2f} x {q:<2} = R${pr*q:>6.2f}\n") # Super formatação: limita a 12 letras de nome para caber alinhado (Estilo Caixa de Mercado)
                f.write("----------------------------------------\n") # Divisória
                f.write(f"TOTAL GASTO:             R${self.total_gasto:>8.2f}\n") # Injeta soma financeira alinhada á direita
                f.write(f"VALOR DISPONÍVEL:        R${self.limite:>8.2f}\n") # Injeta limite inicial alinhado
                f.write( # Imprime string do Saldo
                    f"SALDO RESTANTE:          R${self.limite - self.total_gasto:>8.2f}\n" # Roda matemática na própria emissão
                ) # Fim Escrita
                f.write("----------------------------------------\n") # Decoração
                f.write( # Imprime texto de analise
                    f"PRODUTO MAIS CARO: {produto_caro[0]} (R${produto_caro[1]:.2f})\n" # Preenche com resultado da busca Max(lambda) extraida na linha acima 
                ) # Fim escrita 
                f.write("========================================\n") # Fechamento visual do Cupom

            self.caminho_ultimo_arquivo = caminho # Armazena em variável para o botão ENVIAR saber que arquivo puxar depois!
            self.btn_env.disabled = False # Destrava no sistema o Botão roxinho de compartilhamento 
            self.mostrar_alerta("Sucesso", f"Nota salva em:\n{caminho}") # Mostra onde a nota foi salva
            self.limpar_tela() # Zera tela inteira chamando rotina 

        except Exception as e: # Caso trave (Permissão Negada Android, disco cheio)
            self.mostrar_alerta("Erro", f"Erro ao salvar: {e}") # Reflete código de exceção Python pro usuário resolver

    def compartilhar_nota(self): # Rotina que chama recurso nativo Whatsapp/Emails (Android)
        if not self.caminho_ultimo_arquivo or not os.path.exists( # Trava caso a nota tenha sido sumido pelo usuário logo após salvar
            self.caminho_ultimo_arquivo # Passa check na URL
        ): # Fim IF
            self.mostrar_alerta("Erro", "Arquivo não encontrado!") # Impede tela de falha
            return # Aborta compartilhamento

        try: # Proteção JNIUS Py Android 
            with open(self.caminho_ultimo_arquivo, "r", encoding="utf-8") as file: # Vai lá na pasta e abre agora em formato de Leitura ("r")
                conteudo = file.read() # Suga toda as letras do TXT fiscal para dentro de string

            if autoclass is None: # Se isso for executado num Windows ou Linux e a dependência falhou (linha inicial do App)
                raise ImportError("jnius não disponível") # Gera um gatilho manual jogando o sistema direto pro quadro Exception!

            PythonActivity = autoclass("org.kivy.android.PythonActivity") # Em Android normal: conecta API Jnius ao contexto do Kivy App
            Intent = autoclass("android.content.Intent") # Abre a caixa de construtores de 'Intenção' (Intent) nativo Java Android OS
            String = autoclass("java.lang.String") # Converte dados em memória pro tipo string bruta de Java para não corromper

            intent = Intent(Intent.ACTION_SEND) # Prepara envelope no celular com ordem de disparo de dados genéricos
            intent.setType("text/plain") # Seta tipo de envio como texto puro ASCII pro Android liberar todos Apps
            intent.putExtra(Intent.EXTRA_TEXT, String(conteudo)) # Injeta a nota extraída empacotada no Java (Extra_Text)
            chooser = Intent.createChooser(intent, String("Enviar Nota de Compra")) # Configura tela nativa do celular escolhedora (Compartilhar com...)
            PythonActivity.mActivity.startActivity(chooser) # Comando final: envia Intent ao SO do celular e popa tela em cima do Kivy
        except Exception: # Aterrisa aqui se não estiver no celular
            self.mostrar_alerta( # Popula a janelinha Kivy
                "Info", # Tagzinha
                f"Função de envio via Android.\nCaminho: {self.caminho_ultimo_arquivo}", # E so diz pro usuário onde está o arquivo pra ele ir buscar com o mouse
            ) # Encerra falha 


if __name__ == "__main__": # Ponto inicial que Python aciona quando o script é chamado na linha de comando
    CalculadoraKivyFinal().run() # Inicializa o processo, cria classe App, chama função Build e constrói tudo!