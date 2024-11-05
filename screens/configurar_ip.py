from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

# Import para funções de log
from utils.log_manager import save_log

class ConfigurarIP(Screen):

    def save_ip(self, ip):
        # Salva o IP no arquivo de configuração
        with open("config.txt", "w") as config_file:
            config_file.write(ip)
        save_log("INFO", "ConfigurarIP", "IP configurado com sucesso.")
        MDApp.get_running_app().switch_screen("home_screen")
