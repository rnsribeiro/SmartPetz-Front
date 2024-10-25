import requests
from kivy.uix.screenmanager import Screen
from datetime import datetime
from utils.helpers import get_token, get_ip_address

class CadastrarPetScreen(Screen):

    def salvar_pet(self):
        """Salva o pet com os dados fornecidos."""
        nome_pet = self.ids.nome_pet.text
        tipo_pet = self.ids.tipo_pet.text
        peso_pet = self.ids.peso_pet.text
        tamanho_pet = self.ids.tamanho_pet.text
        idade_pet = self.ids.idade_pet.text

        # Validação simples dos campos
        if not nome_pet or not tipo_pet or not peso_pet or not tamanho_pet or not idade_pet:
            print("Por favor, preencha todos os campos.")
            return

        try:
            peso_pet = float(peso_pet)  # Verifica se o peso é um número válido
            idade_pet = int(idade_pet)  # Verifica se a idade é um número inteiro válido
        except ValueError:
            print("Peso e Idade devem ser números válidos.")
            return

        # Dados para enviar para a API
        data = {
            "name": nome_pet,
            "type_pet": tipo_pet,
            "weight": peso_pet,
            "size": tamanho_pet,
            "age": idade_pet
        }

        # Enviar para a API
        token = get_token()
        ip_address = get_ip_address()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        url = f"http://{ip_address}:8000/pet"

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Pet cadastrado com sucesso.")
            self.manager.current = "home_screen"  # Navegar para a tela inicial após cadastrar o pet
        else:
            print(f"Erro ao cadastrar pet: {response.status_code}")

    def limpar_campos(self):
        """Limpa os campos após o cadastro"""
        self.ids.nome_pet.text = ""
        self.ids.tipo_pet.text = ""
        self.ids.peso_pet.text = ""
        self.ids.tamanho_pet.text = ""
        self.ids.idade_pet.text = ""
