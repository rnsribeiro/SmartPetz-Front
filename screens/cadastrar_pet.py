import requests
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

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

class CadastrarPetScreen(Screen):
    def on_pre_enter(self):
        super().on_pre_enter()      

        # Verifica se o usuário está logado
        token = get_token()
        if not token or not validate_token(token):  
            save_log("ERROR", "HomeScreen", "Usuário não logado.")
            show_error_popup("Favor realizar o login.")          
            MDApp.get_running_app().switch_screen("login")
            return

    def salvar_pet(self):
        """Salva o pet com os dados fornecidos."""
        nome_pet = self.ids.nome_pet.text
        tipo_pet = self.ids.tipo_pet.text
        peso_pet = self.ids.peso_pet.text
        tamanho_pet = self.ids.tamanho_pet.text
        idade_pet = self.ids.idade_pet.text

        # Validação simples dos campos
        if not nome_pet or not tipo_pet or not peso_pet or not tamanho_pet or not idade_pet:
            show_error_popup("Por favor, preencha todos os campos.")
            return

        try:
            peso_pet = float(peso_pet)  # Verifica se o peso é um número válido
            idade_pet = int(idade_pet)  # Verifica se a idade é um número inteiro válido
        except ValueError:
            show_error_popup("Peso e Idade devem ser números válidos.")
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
            show_success_popup("Pet cadastrado com sucesso!")
            save_log("INFO", "CadastrarPetScreen", f"Pet {nome_pet} cadastrado com sucesso")
            MDApp.get_running_app().switch_screen("config")
        else:
            show_error_popup("Erro ao cadastrar pet:" + str(nome_pet))
            save_log("ERROR", "CadastrarPetScreen", f"Erro ao cadastrar o pet {nome_pet}")

    def limpar_campos(self):
        """Limpa os campos após o cadastro"""
        self.ids.nome_pet.text = ""
        self.ids.tipo_pet.text = ""
        self.ids.peso_pet.text = ""
        self.ids.tamanho_pet.text = ""
        self.ids.idade_pet.text = ""
