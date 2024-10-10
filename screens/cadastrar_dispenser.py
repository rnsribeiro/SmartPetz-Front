import os
import requests
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

# Importando funções utilitárias
from utils.helpers import (
    get_ip_address, 
    save_token, 
    get_token, 
    save_dispenser_code, 
    get_dispenser_code, 
    show_error_popup, 
    show_success_popup
)

class CadastrarDispenser(Screen):
    def cadastrar_dispenser(self, code):
         # Verifica se o campo code está vazio
        if not code:
            show_error_popup("O campo de código não pode estar vazio!")
            return

        # Obtém o IP e o token configurados
        #app = MDApp.get_running_app()
        ip_address = get_ip_address()

        url = f"http://{ip_address}:8000/dispenser"
        data = {
            "code": code,
            "water": 0,
            "food": 0
        }

        headers = {            
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            print(f"Status Code: {response.status_code}, Response: {response.text}")  # Para debug

            if response.status_code == 200:
                #app = MDApp.get_running_app()
                save_dispenser_code(code)
                show_success_popup("Dispenser cadastrado com sucesso!")                
                self.manager.current = "home_screen"
            else:
                # Extrai a mensagem de erro detalhada do JSON de resposta
                error_detail = response.json().get("detail", "Erro desconhecido")
                # Exibe o código de status e o detalhe do erro no popup
                show_error_popup(f"Erro ao cadastrar.\nCódigo de status: {response.status_code}\nDetalhe: {error_detail}")
        except requests.exceptions.RequestException as e:
            show_error_popup(f"Erro de conexão: {e}")

    def configurar_dispenser(self, code):
         # Verifica se o campo code está vazio
        if not code:
            show_error_popup("O campo de código não pode estar vazio!")
            return

        # Obtém o IP e o token configurados
        #app = MDApp.get_running_app()

        try:
            save_dispenser_code(code)
            show_success_popup("Dispenser configurado com sucesso!")                
            self.manager.current = "home_screen"    
        except Exception as e:
            show_error_popup(f"Erro ao cadastrar.\nCódigo de status: {e}")

   