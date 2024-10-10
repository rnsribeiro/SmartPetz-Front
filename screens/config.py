import os
import requests
from kivy.uix.screenmanager import ScreenManager, Screen

from utils.helpers import (
    get_token,
    get_ip_address,
    show_error_popup,   
    show_success_popup  
)

class ConfigScreen(Screen):
    
    def on_pre_enter(self):
        super().on_pre_enter()
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
                #config_screen = self.screen_manager.get_screen('config')
                #config_screen.user_name = user_data['name']  # Atualiza o nome do usuário
            elif response.status_code == 401:
                show_error_popup("Erro de autenticação. Por favor,\nrealize o login novamente.")
                self.manager.current = "login"
            else:
                show_error_popup(f"Erro ao buscar\ninformações do usuário:\n{response.status_code}")
                print("Erro ao buscar informações do usuário:", response.status_code)
        except Exception as e:
            print("Erro ao realizar a requisição:", str(e))

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
            self.manager.current = "login"
        except Exception as e:
            show_error_popup(f"Erro ao limpar dados: {str(e)}")
            print(f"Erro ao limpar dados: {str(e)}")

    def logout(self):
        os.remove("token.txt")      
        show_success_popup("Logout efetuado com sucesso.")
        self.manager.current = "login"