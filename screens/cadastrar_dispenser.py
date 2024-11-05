import requests
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

# Import para funções de log
from utils.log_manager import save_log

# Importando funções utilitárias
from utils.helpers import (
    get_ip_address,
    get_token, 
    validate_token,
    save_dispenser_code,
    show_error_popup, 
    show_success_popup
)

class CadastrarDispenser(Screen):    

    def on_pre_enter(self):
        super().on_pre_enter()               

        # Verifica se o usuário está logado
        token = get_token()
        if not token or not validate_token(token):  
            save_log("ERROR", "HomeScreen", "Usuário não logado.")
            show_error_popup("Favor realizar o login.")                      
            MDApp.get_running_app().switch_screen("login")
            return

    def cadastrar_dispenser(self, code):
         # Verifica se o campo code está vazio
        if not code:
            show_error_popup("O campo de código não pode estar vazio!")
            return

        # Obtém o IP e o token configurados
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
                save_dispenser_code(code)
                show_success_popup("Dispenser cadastrado com sucesso!")
                # Quando um dispenser é cadastrado
                save_log("INFO", "CadastrarDispenser", f"Dispenser {code} cadastrado com sucesso")
                MDApp.get_running_app().switch_screen("home_screen")
            else:
                # Extrai a mensagem de erro detalhada do JSON de resposta
                error_detail = response.json().get("detail", "Erro desconhecido")
                # Exibe o código de status e o detalhe do erro no popup
                show_error_popup(f"Erro ao cadastrar.\nCódigo de status: {response.status_code}\nDetalhe: {error_detail}")
                save_log("ERROR", "CadastrarDispenser", f"Erro ao cadastrar o dispenser: {code}")
        except requests.exceptions.RequestException as e:
            show_error_popup(f"Erro de conexão: {e}")
            save_log("ERROR", "CadastrarDispenser", f"Erro ao cadastrar o dispenser: {code}")

    def configurar_dispenser(self, code):
         # Verifica se o campo code está vazio
        if not code:
            show_error_popup("O campo de código não pode estar vazio!")
            return

        try:
            save_dispenser_code(code)
            show_success_popup("Dispenser configurado com sucesso!")
            # Quando um dispenser é cadastrado
            save_log("INFO", "CadastrarDispenser", f"Dispenser {code} configurado com sucesso")
            MDApp.get_running_app().switch_screen("home_screen")
        except Exception as e:
            show_error_popup(f"Erro ao cadastrar.\nCódigo de status: {e}")
            save_log("ERROR", "CadastrarDispenser", f"Erro ao configurar o dispenser {code}")

   