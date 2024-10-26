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

# Importando as classes de tela
from screens.login import Login
from screens.cadastrar_dispenser import CadastrarDispenser
from screens.reservoir_monitor import ReservoirMonitor
from screens.registrar_usuario import RegistrarUsuario
from screens.configurar_ip import ConfigurarIP
from screens.home_screen import HomeScreen
from screens.registro_alimentacoes import RegistroAlimentacoesScreen
from screens.cadastro_refeicao import CadastroRefeicaoScreen
from screens.config import ConfigScreen
from screens.definir_porcao import DefinirPorcaoScreen
from screens.vacinas import VacinaScreen
from screens.cadastrar_vacina import CadastrarVacinaScreen
from screens.cadastrar_pet import CadastrarPetScreen
from screens.listar_pets import ListarPetsScreen


# Importando funções utilitárias
from utils.helpers import (
    get_ip_address, 
    save_token, 
    get_token, 
    save_dispenser_code, 
    get_dispenser_code
)


# Define o tamanho da janela principal
Window.size = (350, 580)

class SmartPetsz(MDApp):
    dispenser_code_file = "dispenser_code.txt"

    def build(self):
        # Carrega o código do dispenser quando o app inicia
        self.load_dispenser_code()

        # Cria o gerenciador de telas
        self.screen_manager = ScreenManager()

        # Carrega os arquivos KV para as telas
        Builder.load_file("UI/pre_splash.kv")
        Builder.load_file("UI/login.kv")
        Builder.load_file("UI/reservoir_monitor.kv")
        Builder.load_file("UI/registrar_usuario.kv")
        Builder.load_file("UI/cadastrar_dispenser.kv")
        Builder.load_file("UI/configurar_ip.kv")
        Builder.load_file("UI/home_screen.kv")
        Builder.load_file("UI/registro_alimentacoes.kv")
        Builder.load_file("UI/cadastro_refeicao.kv")
        Builder.load_file("UI/config.kv")
        Builder.load_file("UI/definir_porcao.kv")
        Builder.load_file("UI/vacinas.kv")
        Builder.load_file("UI/cadastrar_vacina.kv")
        Builder.load_file("UI/cadastrar_pet.kv")
        Builder.load_file("UI/listar_pets.kv")

        # Adiciona a tela de pré-carregamento
        self.screen_manager.add_widget(Builder.load_file("./UI/pre_splash.kv"))

        # Verifica se o IP já está salvo
        ip_address = get_ip_address()

        # Adiciona as outras telas ao ScreenManager
        self.screen_manager.add_widget(Login(name="login"))
        self.screen_manager.add_widget(RegistrarUsuario(name="registrar_usuario"))
        self.screen_manager.add_widget(HomeScreen(name="home_screen"))
        self.screen_manager.add_widget(ConfigurarIP(name="configurar_ip"))
        self.screen_manager.add_widget(CadastrarDispenser(name="cadastrar_dispenser"))
        self.screen_manager.add_widget(ReservoirMonitor(name="reservoir_monitor"))
        self.screen_manager.add_widget(RegistroAlimentacoesScreen(name="registro_alimentacoes"))
        self.screen_manager.add_widget(CadastroRefeicaoScreen(name="cadastro_refeicao"))
        self.screen_manager.add_widget(ConfigScreen(name="config"))
        self.screen_manager.add_widget(DefinirPorcaoScreen(name="definir_porcao"))
        self.screen_manager.add_widget(VacinaScreen(name="vacinas"))
        self.screen_manager.add_widget(CadastrarVacinaScreen(name="cadastrar_vacina"))
        self.screen_manager.add_widget(CadastrarPetScreen(name="cadastrar_pet"))
        self.screen_manager.add_widget(ListarPetsScreen(name="listar_pets"))


        # Navega para a tela de pré-carregamento ou IP
        self.screen_manager.current = "pre_splash"

        if not ip_address:
            self.screen_manager.current = "configurar_ip"
        else:
            self.screen_manager.current = "pre_splash"
            #self.screen_manager.current = "listar_pets"

        return self.screen_manager
       
    
    def load_dispenser_code(self):
        """Carrega o código do dispenser do arquivo"""
        try:
            with open(self.dispenser_code_file, "r") as f:
                self.dispenser_code = f.read().strip()
        except FileNotFoundError:
            self.dispenser_code = None     

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

    def open_date_picker(self):
        # Função para abrir um seletor de datas (se precisar adicionar)
        pass

SmartPetsz().run()
