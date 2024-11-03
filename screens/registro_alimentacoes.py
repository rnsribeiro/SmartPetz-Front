import requests
from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import mainthread
from kivymd.app import MDApp
from kivy.metrics import dp  # Importando a função dp

# Import para funções de log
from utils.log_manager import save_log

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

class RegistroAlimentacoesScreen(Screen):

    def on_pre_enter(self):
        # Chama a função para buscar as refeições quando a tela for carregada
        self.load_food_schedules()

    def load_food_schedules(self):
        """Carrega a lista de refeições da API e preenche a interface gráfica"""

        ip_address = get_ip_address()
        dispenser_code = get_dispenser_code()
        token = get_token()
        # Defina a URL da API (ajuste conforme necessário)
        url = f"http://{ip_address}:8000/fooding_schedule/"        

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        params = {
            "code": dispenser_code
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                schedules = data.get("schedules", [])
                # Chama a função para atualizar a lista de refeições na interface
                self.update_food_list(schedules)
                save_log("INFO", "RegistroAlimentacoesScreen", "Lista carregada com sucesso.")
            else:
                show_error_popup(f"Erro ao buscar os dados: {response.status_code}")
                save_log("ERROR", "RegistroAlimentacoesScreen", f"Erro ao buscar horários do dispenser {dispenser_code}")
        except Exception as e:
            save_log("ERROR", "RegistroAlimentacoesScreen", f"Erro: {str(e)}")
            print(f"Ocorreu um erro: {str(e)}")

    def delete_food_schedule(self, food_id):
        """Envia uma solicitação para excluir um registro de alimentação"""
        ip_address = get_ip_address()
        token = get_token()
        print(token)
        url = f"http://{ip_address}:8000/fooding_schedule/{food_id}"  # Rota para exclusão

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        try:
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:  # Sucesso na exclusão
                show_success_popup("Registro excluído com sucesso!")
                self.load_food_schedules()  # Atualiza a lista após a exclusão
                save_log("INFO", "RegistroAlimentacoesScreen", f"Registro excluído com id:{food_id}.")
            elif response.status_code == 401:  # Unathorized
                save_log("ERROR", "RegistroAlimentacoesScreen", "Erro de autenticação.")
                show_error_popup("Erro de autenticação. Por favor,\nrealize o login novamente.")
                self.manager.current = "login"
            else:
                show_error_popup(f"Erro ao excluir o registro: {response.status_code}")
                save_log("ERROR", "RegistroAlimentacoesScreen", f"Erro ao excluir o id:{food_id}")
        except Exception as e:
            show_error_popup(f"Erro de conexão: {str(e)}")
            save_log("ERROR", "RegistroAlimentacoesScreen", f"Erro: {str(e)}")


    @mainthread
    def update_food_list(self, schedules):
        """Atualiza a lista de refeições na interface gráfica"""
        self.ids.alimentacao_list.clear_widgets()

        for schedule in schedules:
            food_type = "Alimentação automática" if schedule["type_food"] == "automatica" else "Alimentação manual"
            time = schedule["food_time"]
            amount = schedule.get("amount",
                                  "Desconhecido")  # Pega o valor da porção ou exibe "Desconhecido" se não existir

            # Cria um layout horizontal para conter o item da lista e o botão
            item_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(60))

            # Exibe o tipo de alimentação e a hora, incluindo a quantidade da porção
            list_item = TwoLineListItem(
                text=food_type,
                secondary_text=f"{time} - Porção: {amount}g"  # Exibe a hora e a porção juntas
            )

            # Adiciona o list item ao layout
            item_layout.add_widget(list_item)

            # Adiciona um botão de excluir ao lado do item
            delete_button = MDIconButton(
                icon="delete",
                on_release=lambda x, food_id=schedule["_id"]: self.delete_food_schedule(food_id)
            )

            # Adiciona o botão ao layout
            item_layout.add_widget(delete_button)

            # Adiciona o layout à lista de alimentação
            self.ids.alimentacao_list.add_widget(item_layout)

