from kivy.uix.screenmanager import Screen
from kivy.clock import mainthread
from pymongo import MongoClient
from kivymd.uix.list import ThreeLineListItem
from datetime import datetime
from kivymd.app import MDApp

from utils.helpers import get_token, validate_token, show_error_popup
from utils.log_manager import save_log

# Configuração do MongoDB
client = MongoClient("mongodb://smartpet:smartpet@localhost:27017/")
db = client.smartpet
logs_collection = db.logs

class HistoricoScreen(Screen):

    def on_pre_enter(self):
        # Verifica se o usuário está logado
        token = get_token()
        if not token or not validate_token(token):  
            save_log("ERROR", "HomeScreen", "Usuário não logado.")
            show_error_popup("Favor realizar o login.")                      
            MDApp.get_running_app().switch_screen("login")
            return

        self.load_logs()

    @mainthread
    def load_logs(self):
        """Carrega os logs do banco de dados e exibe na tela."""
        self.ids.log_list.clear_widgets()  # Limpa a lista existente
        # Limita a 30 logs mais recentes, ordenando por timestamp de forma decrescente
        logs = logs_collection.find().sort("timestamp", -1).limit(30)  

        for log in logs:
            # Formata o timestamp
            timestamp = log.get('timestamp')
            if isinstance(timestamp, datetime):
                formatted_timestamp = timestamp.strftime("%d-%m-%Y %H:%M:%S")
            else:
                formatted_timestamp = "Data Inválida"

            level = log.get('level')

            if level == "ERROR":
                color = "#FF0000"  # Red
            elif level == "WARNING":
                color = "#F5D905"  # Yellow
            else:
                color = "#03700b"  # Green for INFO

            item = ThreeLineListItem(
                text=f"[color={color}]Screen: [{log.get('screen')}][/color]",
                secondary_text=f"[color={color}]{log.get('level', 'N/A')} [{formatted_timestamp}][/color]",
                tertiary_text=f"[color={color}]{log.get('message', 'N/A')}[/color]"
            )

            self.ids.log_list.add_widget(item)  # Adiciona o item à lista
