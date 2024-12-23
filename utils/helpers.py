import os
import requests
from kivy.uix.popup import Popup
from kivy.uix.label import Label

def get_ip_address():
    if os.path.exists("config.txt"):
        with open("config.txt", "r") as config_file:
            return config_file.read().strip()
    return None

def save_token(token):
    with open("token.txt", "w") as token_file:
        token_file.write(token)

def get_token():
    if os.path.exists("token.txt"):
        with open("token.txt", "r") as token_file:
            return token_file.read().strip()
    return None

def save_dispenser_code(code):
    with open("dispenser_code.txt", "w") as f:
        f.write(code)

def get_dispenser_code():
    try:
        with open("dispenser_code.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def show_success_popup(message):
    popup = Popup(title='Sucesso',
                  content=Label(text=message),
                  size_hint=(0.8, 0.4))
    popup.open()

def show_error_popup(message):
    popup = Popup(title='Erro',
                  content=Label(text=message),
                  size_hint=(0.8, 0.4))
    popup.open()

def validate_token(token):
    """Valida o token chamando a rota de validação da API."""
    ip_address = get_ip_address()
    url = f"http://{ip_address}:8000/user/me/"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True  # Token válido
        else:
            return False  # Token inválido
    except requests.exceptions.RequestException as e:
        print(f"Erro ao validar o token: {e}")
        return False
