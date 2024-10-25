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

class DefinirPorcaoScreen(Screen):
    def definir_porcao(self, amount):
        # Validação para verificar se os valores estão dentro dos limites
        if not amount:
            show_error_popup("Por favor, preencha todos os campos.")
            return

        try:            
            amount = int(amount)
            
            if amount <= 0:
                show_error_popup("A quantidade de ração deve ser maior que 0.")
                return
        except ValueError:
            show_error_popup("Valores inválidos fornecidos.")
            return

        # Salvar a quantidade de ração em um arquivo
        with open("porcao.txt", "w") as porcao_file:
            porcao_file.write(str(amount))

        show_success_popup("Porção definida com sucesso!")

        # Limpar os campos de entrada
        self.clear_inputs()

        # Redirecionar para a tela de configuração
        self.manager.current = "config"
        
        
    def clear_inputs(self):       
        self.ids.input_amount.text = ""
