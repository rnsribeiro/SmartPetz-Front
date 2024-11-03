import os
import requests
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp

# Import para funções de log
from utils.log_manager import save_log

# Importando funções utilitárias
from utils.helpers import (
    get_ip_address, 
    save_token, 
    get_token, 
    validate_token,
    save_dispenser_code, 
    get_dispenser_code, 
    show_error_popup, 
    show_success_popup
)

class ConfigScreen(Screen):
    
    def on_pre_enter(self):
        super().on_pre_enter()       

        # Verifica se o usuário está logado
        token = get_token()
        if not token or not validate_token(token):  
            save_log("ERROR", "HomeScreen", "Usuário não logado.")
            show_error_popup("Favor realizar o login.")          
            MDApp.get_running_app().switch_screen("login")
            return

        self.get_user_info()

    def get_user_info(self):
        # Pega o token armazenado (assumindo que você tem uma função utilitária para isso)
        token = get_token()
        ip_address = get_ip_address()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            # Faz uma requisição para a API
            response = requests.get(f"http://{ip_address}:8000/user/me/", headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                self.ids.label_username.text = user_data['name']

                save_log("INFO", "ConfigScreen", f"Usuário {user_data['name']} carregado com sucesso.")
                #config_screen = self.screen_manager.get_screen('config')
                #config_screen.user_name = user_data['name']  # Atualiza o nome do usuário
            elif response.status_code == 401:
                show_error_popup("Erro de autenticação. Por favor,\nrealize o login novamente.")
                save_log("ERROR", "ConfigScreen", "Erro de autenticação.")
                MDApp.get_running_app().switch_screen("login")                
            else:
                show_error_popup(f"Erro ao buscar\ninformações do usuário:\n{response.status_code}")
                save_log("ERROR", "ConfigScreen", "Erro ao buscar informações do usuário.")
                print("Erro ao buscar informações do usuário:", response.status_code)
        except Exception as e:
            print("Erro ao realizar a requisição:", str(e))
            save_log("ERROR", "ConfigScreen", f"Erro: {str(e)}")

    def limpar_dados(self):
        try:
            # Lista de arquivos a serem deletados
            arquivos_para_deletar = ["config.txt", "token.txt", "dispenser_code.txt"]

            for arquivo in arquivos_para_deletar:
                if os.path.exists(arquivo):
                    os.remove(arquivo)
                    print(f"{arquivo} removido com sucesso.")
                else:
                    print(f"{arquivo} não encontrado.")

            show_success_popup("Dados limpos com sucesso.")
            save_log("INFO", "ConfigScreen", "Dados limpos com sucesso.")
            MDApp.get_running_app().switch_screen("configurar_ip")
        except Exception as e:
            show_error_popup(f"Erro ao limpar dados: {str(e)}")
            save_log("ERROR", "ConfigScreen", f"Erro ao limpar dados: {str(e)}")

    def logout(self):
        os.remove("token.txt")      
        show_success_popup("Logout efetuado com sucesso.")
        save_log("INFO", "ConfigScreen", "Logout efetuado com sucesso.")
        MDApp.get_running_app().switch_screen("login")