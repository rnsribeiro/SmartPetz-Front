import requests
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty

# Importando funções utilitárias
from utils.helpers import get_ip_address, save_token, get_token, save_dispenser_code, get_dispenser_code

class ReservoirMonitor(Screen):
    water_level = NumericProperty(0)
    food_level = NumericProperty(0)

    def on_pre_enter(self):
        super().on_pre_enter()
        self.update_levels()

    def update_levels(self):
        #app = MDApp.get_running_app()
        ip_address = get_ip_address()
        dispenser_code = get_dispenser_code()

        if not dispenser_code:
            print("Nenhum dispenser codastrado")
            return

        url = f"http://{ip_address}:8000/dispenser/levels/?code={dispenser_code}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.water_level = data["water"]
                self.food_level = data["food"]
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
