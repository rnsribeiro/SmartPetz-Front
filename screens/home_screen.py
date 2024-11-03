import requests
from datetime import datetime
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.properties import NumericProperty

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

class HomeScreen(Screen):
    # Propriedades que representam os níveis de água e ração na tela inicial
    water_level = NumericProperty(100)  # Exemplo de valor inicial
    food_level = NumericProperty(100)   # Exemplo de valor inicial

    def on_pre_enter(self):     
        super().on_pre_enter()        

        # Verifica se o IP foi configurado
        ip_address = get_ip_address()
        if not ip_address:
            save_log("ERROR", "HomeScreen", "IP não configurado.")
            show_error_popup("Favor configurar o IP.")
            # se o IP não estiver configurado, navega para a tela de configuração de IP
            MDApp.get_running_app().switch_screen("configurar_ip")
            return

        # Verifica se o usuário está logado
        token = get_token()
        if not token or not validate_token(token):  
            save_log("ERROR", "HomeScreen", "Usuário não logado.")
            show_error_popup("Favor realizar o login.")          
            MDApp.get_running_app().switch_screen("login")
            return
        
        # Verifica se o dispenser foi configurado
        dispenser_code = get_dispenser_code()
        if not dispenser_code:
            save_log("ERROR", "HomeScreen", "Dispenser não configurado.")
            show_error_popup("Favor configurar o código do dispenser.")
            MDApp.get_running_app().switch_screen("cadastrar_dispenser")
            return        

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

        # Obtém a quantidade de porção
        amount = self.get_amount()

        data = {
            "code": dispenser_code,
            "food_time": food_time,
            "amount": amount,
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
                save_log("INFO", "HomeScreen", f"Refeição cadastrada para às {food_time}")
                show_success_popup("Alimentação programada com sucesso!")
            else:
                show_error_popup(f"Erro ao programar alimentação.\nCódigo de status: {response.status_code}\nNecessário pelo menos 1 minuto de diferença")
                save_log("ERROR", "HomeScreen", "Erro ao programar a alimentação.")
        except requests.exceptions.RequestException as e:
            show_error_popup(f"Erro de conexão: {str(e)}")
            save_log("ERROR", "HomeScreen", f"Erro: {str(e)}")

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
                save_log("INFO", "HomeScreen", "Nível do dispenser atualizado.")
        except requests.exceptions.RequestException as e:
            save_log("ERROR", "HomeScreen", f"Erro: {str(e)}")

    def check_levels(self, *args):
        # Calcula a quantidade necessária para atingir 41% de água e ração
        water_diff = max(0, 41 - self.water_level)
        food_diff = max(0, 41 - self.food_level)

        # Habilita o markup do label
        self.ids.water_warning.markup = True
        self.ids.food_warning.markup = True
        self.ids.quantidade_faltante_label.markup = True

        # Configura o texto e a cor para o nível de água
        if self.water_level < 40:
            self.ids.water_warning.text = f"[color=#FF0000]Nível de água está baixo! Faltam {water_diff}% para o normal.[/color]"
            # self.ids.water_warning.text_color = [1, 0, 0, 1]  # Vermelho
        elif 40 >= self.water_level <= 60:
            self.ids.water_warning.text = "[color=#FFA500]Nível de água está normal.[/color]"
            # self.ids.water_warning.text_color = [1, 1, 0, 1]  # Amarelo
        else:
            self.ids.water_warning.text = "[color=#00FF00]Nível de água está bom![/color]"
            # self.ids.water_warning.text_color = [0, 1, 0, 1]  # Verde

        # Configura o texto e a cor para o nível de ração
        if self.food_level < 40:
            self.ids.food_warning.text = f"[color=#FF0000]Nível de ração está baixo! Faltam {food_diff}% para o normal.[/color]"
            # self.ids.food_warning.text_color = [0.8, 0.2, 0.2, 1]  # Vermelho
        elif 40 <= self.food_level <= 60:
            self.ids.food_warning.text = "[color=#FFA500]Nível de ração está normal.[/color]"
            # self.ids.food_warning.text_color = [1, 1, 0, 1]  # Amarelo
        else:
            self.ids.food_warning.text = "[color=#00FF00]Nível de ração está bom![/color]"
            # self.ids.food_warning.text_color = [0.2, 0.8, 0.2, 1]  # Verde

        # Exibe a quantidade faltante para o nível normal (amarelo)
        if water_diff > 0 or food_diff > 0:
            self.ids.quantidade_faltante_label.text = (
                f"[color=#FFA500]Faltam {water_diff}% de água e {food_diff}% de ração para o nível normal.[/color]"
            )
        else:
            self.ids.quantidade_faltante_label.text = "[color=#00FF00]Níveis de água e ração estão bons.[/color]"

    def get_amount(self):
        """Verifica se existe o arquivo porcao.txt e retorna o valor da porção. Se não existir, retorna 50 como padrão."""
        try:
            with open("porcao.txt", "r") as porcao_file:
                amount = porcao_file.read()
        except FileNotFoundError:
            amount = 50
        return amount