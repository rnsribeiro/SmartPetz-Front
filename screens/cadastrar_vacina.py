import requests
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from datetime import datetime

# Importando funções utilitárias
from utils.helpers import (
    get_ip_address,
    get_token, 
    validate_token,
    show_error_popup, 
    show_success_popup
)

# Import para funções de log
from utils.log_manager import save_log

class CadastrarVacinaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_pet = None  # Inicializa selected_pet

    def on_pre_enter(self):        
        super().on_pre_enter()           

        # Verifica se o usuário está logado
        token = get_token()
        if not token or not validate_token(token):  
            save_log("ERROR", "CadastrarVacinaScreen", "Usuário não logado.")
            show_error_popup("Favor realizar o login.")          
            MDApp.get_running_app().switch_screen("login")
            return

        # Ao carregar a tela, busque os animais do usuário logado
        self.load_animais()

    def load_animais(self):
        token = get_token()
        ip_address = get_ip_address()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://{ip_address}:8000/pet"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pets = response.json()
            if pets:
                self.populate_animal_dropdown(pets)
            else:
                print("Nenhum animal encontrado.")
        else:
            print("Erro ao buscar os animais")

    def populate_animal_dropdown(self, pets):
        """Preenche o dropdown com os animais disponíveis."""
        menu_items = [
            {
                "text": pet["name"],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=pet: self.select_animal(x)
            } for pet in pets
        ]

        self.animal_menu = MDDropdownMenu(
            caller=self.ids.animal_dropdown,
            items=menu_items,
            width_mult=4
        )

    def open_animal_dropdown(self):
        """Abre o dropdown para seleção do animal."""
        self.animal_menu.open()

    def select_animal(self, pet):
        """Ação ao selecionar um animal."""
        self.ids.animal_dropdown.text = pet["name"]
        self.selected_pet = pet  # Define o pet selecionado
        self.animal_menu.dismiss()

    def salvar_vacina(self):
        """Salva a vacina com os dados fornecidos."""
        nome_vacina = self.ids.nome_vacina.text
        data_aplicacao = self.ids.data_aplicacao.text

        # Se o campo data_aplicacao estiver vazio, define a data para o dia atual
        if not data_aplicacao:
            data_aplicacao = datetime.today().strftime('%d-%m-%Y')

        # Validação simples dos campos
        if not nome_vacina:
            show_error_popup("Por favor, preencha todos os campos.")
            return

        # Validar o formato da data
        try:
            data_aplicacao_formatada = datetime.strptime(data_aplicacao, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            show_error_popup("Data inválida. Use o formato DD-MM-YYYY.")
            return

        # Verifique se um pet foi selecionado
        if not self.selected_pet:            
            show_error_popup("Por favor, selecione um animal.")
            return

        # Dados para enviar para a API
        data = {
            "pet_id": self.selected_pet["id"],
            "vaccine_name": nome_vacina,
            "application_date": data_aplicacao_formatada
        }

        # Enviar para a API
        token = get_token()
        ip_address = get_ip_address()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        url = f"http://{ip_address}:8000/vaccine"

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            show_success_popup("Vacina cadastrada com sucesso.")
            save_log("INFO", "CadastrarVacinaScreen", f"Vacina {nome_vacina} cadastrada com sucesso")
            MDApp.get_running_app().switch_screen("vacinas")
        else:
            save_log("ERROR", "CadastrarVacinaScreen", f"Não foi possível cadastrar a vacina {nome_vacina}")            
            show_error_popup("Erro ao cadastrar vacina.")
