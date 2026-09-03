'''from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

class TesteBotoesApp(App):
    def build(self):
        root = BoxLayout(orientation="horizontal", spacing=dp(10), padding=dp(10))

        # Botão verde
        btn_add = Button(
            text="Adicionar",
            background_normal="",
            background_color=(0.4, 0.6, 0.3, 1),  # verde
            font_size="14sp",
            bold=True
        )

        # Botão vermelho
        btn_exc = Button(
            text="Excluir",
            background_normal="",
            background_color=(0.7, 0.3, 0.3, 1),  # vermelho
            font_size="14sp",
            bold=True
        )

        # Botão azul
        btn_sal = Button(
            text="Salvar",
            background_normal="",
            background_color=(0, 0.4, 0.8, 1),  # azul
            font_size="14sp",
            bold=True
        )

        # Botão amarelo
        btn_env = Button(
            text="Enviar",
            background_normal="",
            background_color=(0.8, 0.8, 0, 1),  # amarelo
            font_size="14sp",
            bold=True
        )

        # Adiciona todos ao layout
        root.add_widget(btn_add)
        root.add_widget(btn_exc)
        root.add_widget(btn_sal)
        root.add_widget(btn_env)

        return root

if __name__ == "__main__":
    TesteBotoesApp().run()'''
    
    
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

class TesteBotoesMinimalistaApp(App):
    def build(self):
        root = BoxLayout(orientation="horizontal", spacing=dp(10), padding=dp(10))

        btn_add = Button(
            text="Adicionar",
            background_normal="",
            background_color=(0.2, 0.4, 0.2, 1),  # verde acinzentado
            font_size="14sp",
            bold=True
        )

        btn_exc = Button(
            text="Excluir",
            background_normal="",
            background_color=(0.4, 0.2, 0.2, 1),  # vermelho acinzentado
            font_size="14sp",
            bold=True
        )

        btn_sal = Button(
            text="Salvar",
            background_normal="",
            background_color=(0.2, 0.3, 0.4, 1),  # azul acinzentado
            font_size="14sp",
            bold=True
        )

        btn_env = Button(
            text="Enviar",
            background_normal="",
            background_color=(0.4, 0.4, 0.2, 1),  # amarelo acinzentado
            font_size="14sp",
            bold=True
        )

        root.add_widget(btn_add)
        root.add_widget(btn_exc)
        root.add_widget(btn_sal)
        root.add_widget(btn_env)

        return root

if __name__ == "__main__":
    TesteBotoesMinimalistaApp().run()
