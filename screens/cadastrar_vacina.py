import requests
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import mainthread
from datetime import datetime
from utils.helpers import get_token, get_ip_address  # Funções utilitárias para pegar o IP e o token

API_URL_ANIMAIS = "http://<seu_servidor>/pets"
API_URL_VACINAS = "http://<seu_servidor>/vaccines"


class CadastrarVacinaScreen(Screen):

    def on_pre_enter(self):
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
        self.selected_pet = pet
        self.animal_menu.dismiss()

    def salvar_vacina(self):
        """Salva a vacina com os dados fornecidos."""
        nome_vacina = self.ids.nome_vacina.text
        data_aplicacao = self.ids.data_aplicacao.text

        # Validação simples dos campos
        if not nome_vacina or not data_aplicacao:
            print("Por favor, preencha todos os campos.")
            return

        # Validar o formato da data
        try:
            data_aplicacao_formatada = datetime.strptime(data_aplicacao, '%d-%m-%Y').strftime('%Y-%m-%d')
        except ValueError:
            print("Data inválida. Use o formato DD-MM-YYYY.")
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
            print("Vacina cadastrada com sucesso.")
            self.manager.current = "vacinas"  # Navegar de volta à tela de vacinas
        else:
            print(f"Erro ao cadastrar vacina: {response.status_code}")
