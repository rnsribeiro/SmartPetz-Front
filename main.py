import os
import requests
from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window

# Define o tamanho da janela principal
Window.size = (350, 580)

class Login(Screen):
    def do_login(self, username, password):
        # Obtém o IP configurado usando o método get_running_app()
        app = MDApp.get_running_app()
        ip_address = app.get_ip_address()
        url = f"http://{ip_address}:8000/token"  # Usa o IP configurado
        data = {
            "username": username,
            "password": password
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            # Envia a requisição POST com os dados do login
            response = requests.post(url, data=data, headers=headers)
            print(f"Status Code: {response.status_code}, Response: {response.text}")  # Para debug

            if response.status_code == 200:
                # Se o login for bem-sucedido, recebe o token e navega para a tela 'home_screen'
                token = response.json().get("access_token")
                app.save_token(token)
                print("Login bem-sucedido, token:", token)
                self.manager.current = "home_screen"
            else:
                # Se o login falhar, exibe uma mensagem de erro
                self.show_error_popup(f"Login falhou. Código de status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Exibe erro de conexão
            self.show_error_popup(f"Erro de conexão: {e}")

    def show_error_popup(self, message):
        popup = Popup(title='Erro',
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

class MenuScreen(Screen):
    pass

class CadastrarDispenser(Screen):
    def cadastrar_dispenser(self, code):
         # Verifica se o campo code está vazio
        if not code:
            self.show_error_popup("O campo de código não pode estar vazio!")
            return

        # Obtém o IP e o token configurados
        app = MDApp.get_running_app()
        ip_address = app.get_ip_address()

        url = f"http://{ip_address}:8000/dispenser"
        data = {
            "code": code,
            "water": 0,
            "food": 0
        }

        headers = {            
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            print(f"Status Code: {response.status_code}, Response: {response.text}")  # Para debug

            if response.status_code == 200:
                app = MDApp.get_running_app()
                app.save_dispenser_code(code)
                self.show_success_popup("Dispenser cadastrado com sucesso!")                
                self.manager.current = "home_screen"
            else:
                # Extrai a mensagem de erro detalhada do JSON de resposta
                error_detail = response.json().get("detail", "Erro desconhecido")
                # Exibe o código de status e o detalhe do erro no popup
                self.show_error_popup(f"Erro ao cadastrar.\nCódigo de status: {response.status_code}\nDetalhe: {error_detail}")
        except requests.exceptions.RequestException as e:
            self.show_error_popup(f"Erro de conexão: {e}")

    def configurar_dispenser(self, code):
         # Verifica se o campo code está vazio
        if not code:
            self.show_error_popup("O campo de código não pode estar vazio!")
            return

        # Obtém o IP e o token configurados
        app = MDApp.get_running_app()

        try:
            app.save_dispenser_code(code)
            self.show_success_popup("Dispenser configurado com sucesso!")                
            self.manager.current = "home_screen"    
        except Exception as e:
            self.show_error_popup(f"Erro ao cadastrar.\nCódigo de status: {e}")


    def show_success_popup(self, message):
        popup = Popup(title='Sucesso',
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

    def show_error_popup(self, message):
        popup = Popup(title='Erro',
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

class ReservoirMonitor(Screen):
    water_level = NumericProperty(0)
    food_level = NumericProperty(0)

    def on_pre_enter(self):
        super().on_pre_enter()
        self.update_levels()

    def update_levels(self):
        app = MDApp.get_running_app()
        ip_address = app.get_ip_address()
        dispenser_code = app.get_dispenser_code()

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


class RegistrarUsuario(Screen):
    def registrar_usuario(self, username, name, email, password):
        # Obtém o IP configurado usando o método get_running_app()
        app = MDApp.get_running_app()
        ip_address = app.get_ip_address()
        url = f"http://{ip_address}:8000/user"  # Usa o IP configurado
        data = {
            "username": username,
            "name": name,
            "email": email,
            "password": password
        }

        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            # Envia a requisição POST com os dados do usuário
            response = requests.post(url, json=data, headers=headers)
            print(f"Status Code: {response.status_code}, Response: {response.text}")  # Para debug

            if response.status_code == 200:
                # Se o cadastro for bem-sucedido, exibe uma mensagem de sucesso
                self.show_success_popup("Usuário cadastrado com sucesso!")
                self.manager.current = "login"  # Volta para a tela de login
            else:
                # Se o cadastro falhar, exibe uma mensagem de erro
                self.show_error_popup(f"Erro no cadastro. Código de status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Exibe erro de conexão
            self.show_error_popup(f"Erro de conexão: {e}")

    def show_success_popup(self, message):
        popup = Popup(title='Sucesso',
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

    def show_error_popup(self, message):
        popup = Popup(title='Erro',
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()


class ConfigurarIP(Screen):
    def save_ip(self, ip):
        # Salva o IP no arquivo de configuração
        with open("config.txt", "w") as config_file:
            config_file.write(ip)
        app.go_back_to_pre_splash()  # Volta para a tela de pré-carregamento

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
        app = MDApp.get_running_app()
        ip_address = app.get_ip_address()        
        dispenser_code = app.get_dispenser_code()
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
            "amount": 50
        }

        headers = {
            'Content-Type': 'application/json',
            #'Authorization': f'Bearer {app.get_token()}'
        }

        try:
            # Mudança para POST
            response = requests.post(url, json=data, headers=headers)
            print(f"Status Code: {response.status_code}, Response: {response.text}")
            if response.status_code == 200:
                print("Alimentação programada com sucesso!")
            else:
                self.show_error_popup(f"Erro ao programar alimentação.\nCódigo de status: {response.status_code}")                
        except requests.exceptions.RequestException as e:
            self.show_error_popup(f"Erro de conexão: {e}")

    def show_success_popup(self, message):
        popup = Popup(title='Sucesso',
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

    def show_error_popup(self, message):
        popup = Popup(title='Erro',
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

    def load_dispenser_data(self):
        # Carrega os dados do arquivo de configuração
        app = MDApp.get_running_app()
        dispenser_code = app.get_dispenser_code()
        if dispenser_code:
            self.ids.dispenser_code_label.text = f"Dispenser: {dispenser_code}"
        else:
            self.ids.dispenser_code_label.text = "Nenhum dispenser cadastrado"

    def update_dispenser_levels(self):
        app = MDApp.get_running_app()
        ip_address = app.get_ip_address()
        dispenser_code = app.get_dispenser_code()

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

class SmartPetz(MDApp):
    dispenser_code_file = "dispenser_code.txt"

    def build(self):
        # Carrega o código do dispenser quando o app inicia
        self.load_dispenser_code()

        # Cria o gerenciador de telas
        self.screen_manager = ScreenManager()

        # Carrega os arquivos KV para as telas
        Builder.load_file("./UI/pre_splash.kv")
        Builder.load_file("./UI/login.kv")
        Builder.load_file("./UI/reservoir_monitor.kv")
        Builder.load_file("./UI/registrar_usuario.kv")
        Builder.load_file("./UI/cadastrar_dispenser.kv")
        Builder.load_file("./UI/configurar_ip.kv")
        Builder.load_file("./UI/home_screen.kv")
        Builder.load_file("./UI/menu.kv")


         # Adiciona a tela de pré-carregamento
        self.screen_manager.add_widget(Builder.load_file("./UI/pre_splash.kv"))

       # Verifica se o IP já está salvo
        ip_address = self.get_ip_address()  # Obtém o IP

        # Adiciona as outras telas ao ScreenManager
        self.screen_manager.add_widget(Login(name="login"))
        self.screen_manager.add_widget(RegistrarUsuario(name="registrar_usuario"))
        self.screen_manager.add_widget(HomeScreen(name="home_screen"))
        self.screen_manager.add_widget(MenuScreen(name="menu_screen"))
        self.screen_manager.add_widget(ConfigurarIP(name="configurar_ip"))
        self.screen_manager.add_widget(CadastrarDispenser(name="cadastrar_dispenser"))
        self.screen_manager.add_widget(ReservoirMonitor(name="reservoir_monitor"))
        self.screen_manager.current = "pre_splash"  # Navega para a tela de pré-carregamento

        if not ip_address:
            self.screen_manager.current = "configurar_ip"
        else:
            self.screen_manager.current = "pre_splash"

        return self.screen_manager

    def save_dispenser_code(self, code):
        """Salva o código do dispenser em um arquivo"""        
        with open(self.dispenser_code_file, "w") as f:
            f.write(code)
        self.dispenser_code = code    

    def load_dispenser_code(self):
        """Carrega o código do dispenser do arquivo"""
        try:
            with open(self.dispenser_code_file, "r") as f:
                self.dispenser_code = f.read().strip()
        except FileNotFoundError:
            self.dispenser_code = None

    def get_dispenser_code(self):
        """Retorna o código do dispenser"""
        return self.dispenser_code    

    def switch_screen(self, screen_name):
        """Método para trocar entre as telas"""
        self.screen_manager.current = screen_name

    def sair_do_app(self):
        """Função para fechar o aplicativo"""
        self.stop()  # Para fechar o aplicativo

    def is_ip_configured(self):
        # Verifica se o IP já foi configurado (simula com um arquivo)
        return os.path.exists("config.txt")

    def save_ip(self, ip):
        # Salva o IP no arquivo de configuração
        with open("config.txt", "w") as config_file:
            config_file.write(ip)
        self.go_back_to_pre_splash()

    def get_token(self):
        # Adicione lógica para salvar e obter o token após o login
        if os.path.exists("token.txt"):
            with open("token.txt", "r") as token_file:
                return token_file.read().strip()
        return None

    def save_token(self, token):
        # Salva o token no arquivo de configuração
        with open("token.txt", "w") as token_file:
            token_file.write(token)

    def get_ip_address(self):
        # Lê o IP do arquivo de configuração, se existir
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as config_file:
                return config_file.read().strip()  # Remove espaços em branco
        return None

    def go_back_to_login(self):
        # Volta para a tela de login
        self.root.current = "login"

    def go_back_to_pre_splash(self):
        # Volta para a tela de pré-carregamento
        self.screen_manager.current = "pre_splash"

    def go_to_registrar(self):
        # Vai para a tela de registro de usuário
        self.screen_manager.current = "registrar_usuario"

    def go_back_to_home(self):
        # Volta para a tela de Definir Porção
        self.root.current = "home_screen"    

SmartPetz().run()
