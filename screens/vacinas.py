import requests
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import TwoLineListItem
from kivy.clock import mainthread
from utils.helpers import get_token, get_ip_address  # Supondo que você tenha essas funções utilitárias

API_URL_ANIMAIS = "http://<seu_servidor>/pets"
API_URL_VACINAS = "http://<seu_servidor>/vaccines"

class VacinaScreen(Screen):

    def on_pre_enter(self):
        # Ao carregar a tela, busque os animais do usuário logado
        self.load_animais()

    def load_animais(self):
        # Requisição para buscar os animais do usuário logado
        token = get_token()  # Obter token de autenticação
        ip_address = get_ip_address()  # Obter IP do servidor
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://{ip_address}:8000/pet"  # Ajustar a URL da API

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pets = response.json()  # Supondo que a resposta seja uma lista de animais
            if pets:
                # Popula o dropdown com a lista de animais
                self.populate_animal_dropdown(pets)
                # Seleciona automaticamente o primeiro animal da lista
                first_pet = pets[0]
                self.select_animal(first_pet)
            else:
                print("Nenhum animal encontrado.")
        else:
            print("Erro ao buscar os animais")

    def populate_animal_dropdown(self, pets):
        """Cria o menu dropdown com a lista de animais."""
        menu_items = [
            {
                "text": pet["name"],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=pet: self.select_animal(x)
            } for pet in pets
        ]

        self.animal_menu = MDDropdownMenu(
            caller=self.ids.pet_dropdown,
            items=menu_items,
            width_mult=4
        )

        # Permite abrir o dropdown quando o usuário clica
        self.ids.pet_dropdown.on_release = self.animal_menu.open

    def select_animal(self, pet):
        """Ação ao selecionar um animal no dropdown."""
        self.ids.pet_dropdown.text = pet["name"]

        # Verifica se o menu foi criado e fecha o dropdown após a seleção
        if hasattr(self, 'animal_menu'):
            self.animal_menu.dismiss()

        # Carrega as vacinas para o animal selecionado
        self.load_vacinas(pet["id"])

    def load_vacinas(self, pet_id):
        """Requisição para carregar as vacinas do animal selecionado."""
        token = get_token()
        ip_address = get_ip_address()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://{ip_address}:8000/vaccine/{pet_id}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            vacinas = response.json()
            self.update_vacina_list(vacinas)
        else:
            print("Erro ao buscar as vacinas")

    @mainthread
    def update_vacina_list(self, vacinas):
        """Atualiza a lista de vacinas na interface."""
        self.ids.vacina_list.clear_widgets()

        for vacina in vacinas:
            item = TwoLineListItem(
                text=vacina["vaccine_name"],
                secondary_text=f"Aplicado em: {vacina['application_date']}"
            )
            self.ids.vacina_list.add_widget(item)
