import requests
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineListItem
from kivy.clock import mainthread
from kivy.metrics import dp
from utils.helpers import get_token, get_ip_address  # Supondo que você tenha essas funções utilitárias

# Import para funções de log
from utils.log_manager import save_log

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
                save_log("INFO", "VacinaScreen", "Lista de pets carregada com sucesso.")
            else:
                print("Nenhum animal encontrado.")
                save_log("INFO", "VacinaScreen", "Nenhum pet encontrado.")
        else:
            print("Erro ao buscar os animais")
            save_log("ERROR", "VacinaScreen", "Erro ao buscar os pets.")

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

    def delete_vacina(self, vaccine_id):
        """Exclui uma vacina pelo ID"""
        token = get_token()
        ip_address = get_ip_address()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://{ip_address}:8000/vaccine/{vaccine_id}"

        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print("Vacina excluída com sucesso!")
            save_log("INFO", "VacinaScreen", f"Vacina excluída com id:{vaccine_id}.")
            self.on_pre_enter()  # Recarrega as vacinas após a exclusão
        else:
            save_log("ERROR", "VacinaScreen", f"Erro ao excluir a vacina com id:{vaccine_id}")
            print(f"Erro ao excluir vacina: {response.status_code}")

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
            save_log("INFO", "VacinaScreen", f"Vacinas carregadas com sucesso.")
        else:
            save_log("ERROR", "VacinaScreen", "Erro ao buscar as vacinas.")
            print("Erro ao buscar as vacinas")

    @mainthread
    def update_vacina_list(self, vacinas):
        """Atualiza a lista de vacinas na interface."""
        self.ids.vacina_list.clear_widgets()

        for vacina in vacinas:
            # Converte a data do formato "YYYY-MM-DD" para "DD-MM-YYYY"
            data_aplicacao = datetime.strptime(vacina['application_date'], '%Y-%m-%d').strftime('%d-%m-%Y')

            # Define o status com base na data de aplicação
            hoje = datetime.today().date()
            if datetime.strptime(vacina['application_date'], '%Y-%m-%d').date() > hoje:
                status = "[color=#FFA500]Pendente[/color]"  # Amarelo para pendente
            else:
                status = "[color=#00FF00]Concluído[/color]"  # Verde para concluído

            # Cria um layout horizontal para conter o item da lista e o botão
            item_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(60))

            # Exibe o nome da vacina, status e a data de aplicação
            item = TwoLineListItem(
                text=f"{vacina['vaccine_name']} - {status}",
                secondary_text=f"Aplicado em: {data_aplicacao}"
            )

            # Adiciona o item ao layout
            item_layout.add_widget(item)

            # Adiciona um botão de excluir ao lado do item
            delete_button = MDIconButton(
                icon="delete",
                on_release=lambda x, vaccine_id=vacina["id"]: self.delete_vacina(vaccine_id)
            )

            # Adiciona o botão ao layout
            item_layout.add_widget(delete_button)
            
            # Agora adiciona o layout completo à lista de vacinas
            self.ids.vacina_list.add_widget(item_layout)
