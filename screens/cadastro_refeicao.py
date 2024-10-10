from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
import requests
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label

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

class CadastroRefeicaoScreen(Screen):
    def cadastrar_refeicao(self, hour, minute, amount):
        # Validação para verificar se os valores estão dentro dos limites
        if not hour or not minute or not amount:
            show_error_popup("Por favor, preencha todos os campos.")
            return

        try:
            hour = int(hour)
            minute = int(minute)
            amount = int(amount)
            
            if not (0 <= hour < 24):
                show_error_popup("A hora deve estar entre 00 e 23.")
                return
            
            if not (0 <= minute < 60):
                show_error_popup("Os minutos devem estar entre 00 e 59.")
                return
            
            if amount <= 0:
                show_error_popup("A quantidade de ração deve ser maior que 0.")
                return
        except ValueError:
            show_error_popup("Valores inválidos fornecidos.")
            return

        ip_address = get_ip_address()
        token = get_token()
        dispenser_code = get_dispenser_code()

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
                app = MDApp.get_running_app()             
                app.switch_screen("registro_alimentacoes")
                self.clear_inputs()
            elif response.status_code == 401:  # Unathorized
                show_error_popup("Erro de autenticação. Por favor,\nrealize o login novamente.")
                self.manager.current = "login"
            else:
                show_error_popup(f"Erro ao cadastrar a refeição: {response.text}")
        except Exception as e:
            show_error_popup(f"Erro de conexão: {str(e)}")

    def clear_inputs(self):
        self.ids.input_hour.text = ""
        self.ids.input_minute.text = ""
        self.ids.input_amount.text = ""
