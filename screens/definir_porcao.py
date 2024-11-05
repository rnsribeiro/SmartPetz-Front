from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

# Import para funções de log
from utils.log_manager import save_log

# Importando funções utilitárias
from utils.helpers import (
    get_token,
    validate_token,
    show_error_popup,
    show_success_popup
)

class DefinirPorcaoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.porcao_menu = None
        self.porcoes_predefinidas = ["25g", "50g", "75g", "100g", "125g", "150g"]

    def on_pre_enter(self):
        # Verifica se o usuário está logado
        token = get_token()
        if not token or not validate_token(token):  
            save_log("ERROR", "HomeScreen", "Usuário não logado.")
            show_error_popup("Favor realizar o login.")                      
            MDApp.get_running_app().switch_screen("login")
            return
            
        # Configura o menu de porções
        self.porcao_menu = MDDropdownMenu(
            caller=self.ids.porcao_dropdown,
            items=[
                {"text": porcao, "viewclass": "OneLineListItem", "on_release": lambda x=porcao: self.select_porcao(x)}
                for porcao in self.porcoes_predefinidas
            ],
            width_mult=4
        )

    def open_porcao_menu(self):
        # Abre o menu de porção
        if self.porcao_menu:
            self.porcao_menu.open()

    def select_porcao(self, porcao):
        # Define a porção selecionada no dropdown e fecha o menu
        self.ids.porcao_dropdown.text = porcao
        self.porcao_menu.dismiss()

    def salvar_porcao(self):
        # Função para salvar a porção selecionada
        porcao_selecionada = self.ids.porcao_dropdown.text
        if porcao_selecionada == "Selecione a porção":
            show_error_popup("Por favor, selecione uma porção.")            
            return

        try:
            with open("porcao.txt", "w") as porcao_file:
                porcao_file.write(porcao_selecionada.replace("g", ""))
            save_log("INFO", "DefinirPorcaoScreen", f"Porção de {porcao_selecionada}g salva com sucesso")
            show_success_popup(f"Porção de {porcao_selecionada} salva com sucesso.")
            MDApp.get_running_app().switch_screen("config")
        except Exception as e:
            save_log("ERROR", "DefinirPorcaoScreen", f"Erro ao salvar a porção: {str(e)}")
