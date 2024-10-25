import requests
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineListItem
from kivy.clock import mainthread
from kivy.metrics import dp
from utils.helpers import get_token, get_ip_address  # Funções utilitárias para pegar o IP e o token


class ListarPetsScreen(Screen):

    def on_pre_enter(self):
        # Ao carregar a tela, busque os pets do usuário logado
        self.load_pets()

    def load_pets(self):
        token = get_token()
        ip_address = get_ip_address()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://{ip_address}:8000/pet"  # A rota para listar os pets

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pets = response.json()
            self.update_pet_list(pets)
        else:
            print("Erro ao buscar os pets")

    @mainthread
    def update_pet_list(self, pets):
        """Atualiza a lista de pets na interface."""
        self.ids.pets_list.clear_widgets()

        for pet in pets:
            # Cria um layout horizontal para conter o item da lista e o botão
            item_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(60))

            # Exibe o nome do pet e o tipo de pet
            item = TwoLineListItem(
                text=pet['name'],
                secondary_text=f"Tipo: {pet['type_pet']} - Idade: {pet['age']} anos"
            )

            # Adiciona o item ao layout
            item_layout.add_widget(item)

            # Adiciona um botão de excluir ao lado do item
            delete_button = MDIconButton(
                icon="delete",
                on_release=lambda x, pet_id=pet["id"]: self.delete_pet(pet_id)
            )

            # Adiciona o botão ao layout
            item_layout.add_widget(delete_button)

            # Agora adiciona o layout completo à lista de pets
            self.ids.pets_list.add_widget(item_layout)

    def delete_pet(self, pet_id):
        """Exclui um pet pelo ID"""
        token = get_token()
        ip_address = get_ip_address()
        headers = {"Authorization": f"Bearer {token}"}
        url = f"http://{ip_address}:8000/pet/{pet_id}"  # Rota para deletar o pet

        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            print("Pet excluído com sucesso!")
            self.load_pets()  # Recarrega a lista de pets após a exclusão
        else:
            print(f"Erro ao excluir pet: {response.status_code}")
