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

class ConfigurarIP(Screen):

    def save_ip(self, ip):
        # Salva o IP no arquivo de configuração
        with open("config.txt", "w") as config_file:
            config_file.write(ip)
        save_log("INFO", "ConfigurarIP", "IP configurado com sucesso.")
        MDApp.get_running_app().switch_screen("home_screen")
