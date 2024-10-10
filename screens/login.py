from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import requests
from kivymd.app import MDApp

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

class Login(Screen):
    def do_login(self, username, password):
        # Obtém o IP configurado usando o método get_running_app()
        #app = MDApp.get_running_app()
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
                print("Login bem-sucedido, token:", token)
                show_success_popup("Usuário logado com sucesso!")
                self.manager.current = "home_screen"
            else:
                # Se o login falhar, exibe uma mensagem de erro
                show_error_popup(f"Login falhou. Código de status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Exibe erro de conexão
            show_error_popup(f"Erro de conexão: {e}")
    