import os
import logging
from kivymd.app import MDApp
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
from screens.historico import HistoricoScreen

# Import para funções de log
from utils.log_manager import save_log

# Importando funções utilitárias
from utils.helpers import (
    get_ip_address
)


# Define o tamanho da janela principal
Window.size = (350, 580)


logging.basicConfig(level=logging.INFO)

class SmartPetsz(MDApp):
    dispenser_code_file = "dispenser_code.txt"

    def build(self):
        save_log("INFO", "SmartPetsz", "Iniciando app...")
        save_log("INFO", "SmartPetsz", "Carregando arquivos de configuração...")
        # Carrega o código do dispenser quando o app inicia
        self.load_dispenser_code()
        # Verifica se o IP já está salvo
        ip_address = get_ip_address()

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
        Builder.load_file("UI/historico.kv")

        # Adiciona a tela de pré-carregamento
        self.screen_manager.add_widget(Builder.load_file("./UI/pre_splash.kv"))

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
        self.screen_manager.add_widget(HistoricoScreen(name="historico"))
        save_log("INFO", "SmartPetsz", "Telas inicializadas...")

        # Armazena as referências dos itens do Bottom Navigation
        self.nav_items = {
            'home_screen': 'nav_home',
            'vacinas': 'nav_vacina',
            'registro_alimentacoes': 'nav_registros',
            'reservoir_monitor': 'nav_monitor',
            'config': 'nav_config'
        }

        # Navega para a tela de pré-carregamento ou IP
        self.switch_screen("pre_splash")        
           
        return self.screen_manager
       
    
    def load_dispenser_code(self):
        """Carrega o código do dispenser do arquivo"""
        try:
            with open(self.dispenser_code_file, "r") as f:
                self.dispenser_code = f.read().strip()
            save_log("INFO", "SmartPetsz", "Configurando o dispenser.")
        except FileNotFoundError:
            self.dispenser_code = None
            save_log("ERROR", "SmartPetsz", "Dispenser não configurado.")

    def switch_screen(self, screen_name):
        # Altera a tela atual
        self.screen_manager.current = screen_name
        save_log("INFO", "SmartPetsz", f"Mudando para a tela: {screen_name}")

        # Atualiza a cor dos itens do Bottom Navigation para mostrar o item ativo
        active_color = [0, 0.5, 1, 1]  # Azul
        inactive_color = [0, 0, 0, 1]  # Preto

        # Reseta a cor de todos os itens para inativo
        for item in self.nav_items.values():
            if hasattr(self.root, item):
                getattr(self.root, item).text_color = inactive_color

        # Define a cor do item ativo
        if screen_name in self.nav_items:
            active_item_id = self.nav_items[screen_name]
            if hasattr(self.root, active_item_id):
                getattr(self.root, active_item_id).text_color = active_color

    def sair_do_app(self):
        """Função para fechar o aplicativo"""
        save_log("INFO", "SmartPetsz", "Finalizando o aplicativo...")
        self.stop()  # Para fechar o aplicativo

    def is_ip_configured(self):
        # Verifica se o IP já foi configurado (simula com um arquivo)
        return os.path.exists("config.txt")

    def save_ip(self, ip):
        # Salva o IP no arquivo de configuração
        with open("config.txt", "w") as config_file:
            config_file.write(ip)
        save_log("INFO", "SmartPetsz", "IP configurado com sucesso.")
        self.switch_screen("home_screen")   

SmartPetsz().run()
