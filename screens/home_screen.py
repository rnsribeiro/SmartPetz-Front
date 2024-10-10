import requests
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivymd.app import MDApp  # Certifique-se de importar MDApp

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

class HomeScreen(Screen):
    # Propriedades que representam os níveis de água e ração na tela inicial
    water_level = NumericProperty(100)  # Exemplo de valor inicial
    food_level = NumericProperty(100)   # Exemplo de valor inicial

    def on_pre_enter(self):     
        super().on_pre_enter()
        self.load_dispenser_data()          
        self.update_dispenser_levels()
        # Bind as propriedades water_level e food_level ao método check_levels
        self.bind(water_level=self.check_levels, food_level=self.check_levels)
        self.check_levels()  # Executa check_levels quando a tela é exibida

    def create_fooding_schedule(self):
        #app = MDApp.get_running_app()  # Certifique-se de obter a instância do app
        ip_address = get_ip_address()        
        dispenser_code = get_dispenser_code()
        token = get_token()
        print(dispenser_code)

        if not dispenser_code:
            print("Nenhum dispenser cadastrado")
            return

        url = f"http://{ip_address}:8000/fooding_schedule/"

        # Obtendo a hora atual e formatando como "HH:MM"
        food_time = datetime.now().strftime("%H:%M")  # Formato 'HH:MM'

        data = {
            "code": dispenser_code,
            "food_time": food_time,
            "amount": 50,
            "type_food": "manual"
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        try:
            # Mudança para POST
            response = requests.post(url, json=data, headers=headers)
            print(f"Status Code: {response.status_code}, Response: {response.text}")
            if response.status_code == 200:
                show_success_popup("Alimentação programada com sucesso!")
                print("Alimentação programada com sucesso!")
            else:
                show_error_popup(f"Erro ao programar alimentação.\nCódigo de status: {response.status_code}\nNecessário pelo menos 1 hora de diferença")                
        except requests.exceptions.RequestException as e:
            show_error_popup(f"Erro de conexão: {e}")

    def load_dispenser_data(self):
        # Obtém a instância do aplicativo
        #app = MDApp.get_running_app()
        dispenser_code = get_dispenser_code()
        if dispenser_code:
            self.ids.dispenser_code_label.text = f"Dispenser: {dispenser_code}"
        else:
            self.ids.dispenser_code_label.text = "Nenhum dispenser cadastrado"

    def update_dispenser_levels(self):
        #app = MDApp.get_running_app()
        ip_address = get_ip_address()
        dispenser_code = get_dispenser_code()

        if not dispenser_code:
            print("Nenhum dispenser cadastrado")
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

    def check_levels(self, *args):
        # Calcula a quantidade necessária para atingir 41% de água e ração
        water_diff = max(0, 41 - self.water_level)
        food_diff = max(0, 41 - self.food_level)
        
        # Configura o texto e a cor para o nível de água
        if self.water_level < 40:
            self.ids.water_warning.text = f"Nível de água está baixo! Faltam {water_diff}% para o normal."
            self.ids.water_warning.text_color = [1, 0, 0, 1]  # Vermelho
        elif 40 >= self.water_level <= 60:
            self.ids.water_warning.text = "Nível de água está normal."
            self.ids.water_warning.text_color = [1, 1, 0, 1]  # Amarelo
        else:
            self.ids.water_warning.text = "Nível de água está bom!"
            self.ids.water_warning.text_color = [0, 1, 0, 1]  # Verde

        # Configura o texto e a cor para o nível de ração
        if self.food_level < 40:
            self.ids.food_warning.text = f"Nível de ração está baixo! Faltam {food_diff}% para o normal."
            self.ids.food_warning.text_color = [0.8, 0.2, 0.2, 1]  # Vermelho
        elif 40 <= self.food_level <= 60:
            self.ids.food_warning.text = "Nível de ração está normal."
            self.ids.food_warning.text_color = [1, 1, 0, 1]  # Amarelo
        else:
            self.ids.food_warning.text = "Nível de ração está bom!"
            self.ids.food_warning.text_color = [0.2, 0.8, 0.2, 1]  # Verde

        # Exibe a quantidade faltante para o nível normal (amarelo)
        if water_diff > 0 or food_diff > 0:
            self.ids.quantidade_faltante_label.text = (
                f"Faltam {water_diff}% de água e {food_diff}% de ração para o nível normal (amarelo)."
            )
        else:
            self.ids.quantidade_faltante_label.text = "Níveis de água e ração estão no normal e bom."
