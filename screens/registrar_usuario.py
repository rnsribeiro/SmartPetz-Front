import requests
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import (
    ScreenManager, 
    Screen
)

# Import para funções de log
from utils.log_manager import save_log

# Importando funções utilitárias
from utils.helpers import (
    get_ip_address, 
    save_token, get_token, 
    save_dispenser_code, 
    get_dispenser_code, 
    show_error_popup, 
    show_success_popup
)

class RegistrarUsuario(Screen):
    def registrar_usuario(self, username, name, email, password, confirm_password):
        # Obtém o IP configurado usando o método get_running_app()
        #app = MDApp.get_running_app()

        if password != confirm_password:
            show_error_popup("As senhas são diferentes!")
            return

        # Verifica se o campo username está vazio

        ip_address = get_ip_address()
        url = f"http://{ip_address}:8000/user"  # Usa o IP configurado
        data = {
            "username": username,
            "name": name,
            "email": email,
            "password": password
        }

        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            # Envia a requisição POST com os dados do usuário
            response = requests.post(url, json=data, headers=headers)
            print(f"Status Code: {response.status_code}, Response: {response.text}")  # Para debug

            if response.status_code == 200:
                # Se o cadastro for bem-sucedido, exibe uma mensagem de sucesso
                show_success_popup("Usuário cadastrado com sucesso!")
                save_log("INFO", "RegistrarUsuario", "Usuário registrado com sucesso.")
                self.manager.current = "login"  # Volta para a tela de login
            else:
                # Se o cadastro falhar, exibe uma mensagem de erro
                show_error_popup(f"Erro ao cadastrar.\nCódigo de status: {response.status_code}\n{response.text}")
                save_log("ERROR", "RegistrarUsuario", "Erro ao registrar usuário.")
        except requests.exceptions.RequestException as e:
            # Exibe erro de conexão
            save_log("ERROR", "RegistrarUsuario", f"Erro: {str(e)}")
            show_error_popup(f"Erro de conexão: {str(e)}")

    