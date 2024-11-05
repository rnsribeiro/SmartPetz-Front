from kivy.uix.screenmanager import Screen
import requests
from kivymd.app import MDApp

# Import para funções de log
from utils.log_manager import save_log

# Importando funções utilitárias
from utils.helpers import (
    get_ip_address, 
    save_token, 
    show_error_popup,
)

class Login(Screen):

    def do_login(self, username, password):       

        ip_address = get_ip_address()
        url = f"http://{ip_address}:8000/token"  # Usa o IP configurado
        data = {
            "username": username,
            "password": password
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            # Envia a requisição POST com os dados do login
            response = requests.post(url, data=data, headers=headers)
            print(f"Status Code: {response.status_code}, Response: {response.text}")  # Para debug

            if response.status_code == 200:
                # Se o login for bem-sucedido, recebe o token e navega para a tela 'home_screen'
                token = response.json().get("access_token")
                save_token(token)                
                save_log("INFO", "Login", "Usuário logado com sucesso.")
                MDApp.get_running_app().switch_screen("home_screen")
            else:
                # Se o login falhar, exibe uma mensagem de erro
                show_error_popup(f"Login falhou. Código de status: {response.status_code}")
                save_log("ERROR", "Login", "Erro ao realizar o login")
        except requests.exceptions.RequestException as e:
            # Exibe erro de conexão
            save_log("ERROR", "Login", f"Erro: {str(e)}")
            show_error_popup(f"Erro de conexão: {str(e)}")
    