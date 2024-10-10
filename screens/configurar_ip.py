from kivy.uix.screenmanager import ScreenManager, Screen

class ConfigurarIP(Screen):
    def save_ip(self, ip):
        # Salva o IP no arquivo de configuração
        with open("config.txt", "w") as config_file:
            config_file.write(ip)
        app.go_back_to_pre_splash()  # Volta para a tela de pré-carregamento
