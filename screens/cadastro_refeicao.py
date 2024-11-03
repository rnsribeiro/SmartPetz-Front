from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
import requests
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label

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

class CadastroRefeicaoScreen(Screen):

    def on_pre_enter(self):
        super().on_pre_enter()   

        # Verifica se o usuário está logado
        token = get_token()
        if not token or not validate_token(token):  
            save_log("ERROR", "HomeScreen", "Usuário não logado.")
            show_error_popup("Favor realizar o login.")          
            MDApp.get_running_app().switch_screen("login")
            return

    def cadastrar_refeicao(self, hour, minute):
        # Validação para verificar se os valores estão dentro dos limites
        if not hour or not minute:
            show_error_popup("Por favor, preencha todos os campos.")
            return

        try:
            hour = int(hour)
            minute = int(minute)

            # Obter o valor da porção usando a função get_amount
            amount = self.get_amount()

            if not (0 <= hour < 24):
                show_error_popup("A hora deve estar entre 00 e 23.")
                return
            
            if not (0 <= minute < 60):
                show_error_popup("Os minutos devem estar entre 00 e 59.")
                return            
            
        except ValueError:
            show_error_popup("Valores inválidos fornecidos.")
            return

        ip_address = get_ip_address()
        token = get_token()
        dispenser_code = get_dispenser_code()
        # Cria uma instância do aplicativo
        app = MDApp.get_running_app()

        # URL da sua API
        url = f'http://{ip_address}:8000/fooding_schedule/'

        # Headers da requisição
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        # Formata a hora como HH:MM
        food_time = f"{str(hour).zfill(2)}:{str(minute).zfill(2)}"

        # Dados para enviar
        data = {
            "code": dispenser_code,
            "food_time": food_time,
            "amount": amount,
            "type_food": "automatica"
        }

        # Enviando a requisição
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:  # Sucesso
                show_success_popup("Refeição cadastrada com sucesso!")
                save_log("INFO", "CadastroRefeicaoScreen", f"Refeição cadastrada para {food_time}")                             
                MDApp.get_running_app().switch_screen("registro_alimentacoes")
                self.clear_inputs()
            elif response.status_code == 401:  # Unauthorized
                show_error_popup("Erro de autenticação. Por favor,\nrealize o login novamente.")
                self.manager.current = "login"
            else:
                show_error_popup(f"Erro ao cadastrar a refeição: {response.text}")
                save_log("ERROR", "CadastroRefeicaoScreen", f"Erro ao cadastrar a refeição para {food_time}")
        except Exception as e:
            save_log("ERROR", "CadastroRefeicaoScreen", f"Erro de conexão: {str(e)}")
            show_error_popup(f"Erro de conexão: {str(e)}")

    def clear_inputs(self):
        self.ids.input_hour.text = ""
        self.ids.input_minute.text = ""

    def get_amount(self):
        """Verifica se existe o arquivo porcao.txt e retorna o valor da porção. Se não existir, retorna 50 como padrão."""
        try:
            with open("porcao.txt", "r") as porcao_file:
                amount = porcao_file.read()
        except FileNotFoundError:
            amount = 50
        return amount
