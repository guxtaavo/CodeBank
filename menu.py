from pessoa import Pessoa
from cliente import Cliente
from conta import Conta
from endereco import Endereco
from data import DatabaseManager
from pathlib import Path
import sys

class Menu:
    def __init__(self):
        self.main_menu()

    def main_menu(self):
        while True:
            print("\nMenu Principal")
            print("1. Adicionar novo cliente")
            print("2. Login")
            print("3. Sair")
            choice = input("Escolha uma opção: ")

            if choice == '1':
                self.add_new_client()
            elif choice == '2':
                self.login()
            elif choice == '3':
                sys.exit()
            else:
                print("Opção inválida. Tente novamente.")

    def add_new_client(self):
        print("\nAdicionar Novo Cliente")

        nome = input("Nome: ")
        cpf = input("CPF: ")
        data_nascimento = input("Data de Nascimento (DD/MM/AAAA): ")

        cep = input("CEP: ")

        email = input("Email: ")
        senha = input("Senha: ")

        pessoa = Pessoa(nome, cpf, data_nascimento)
        endereco = Endereco(cep)
        conta = Conta(email, senha, None, None)
        cliente = Cliente(pessoa, endereco, conta)

        ROOT_DIR = Path(__file__).parent
        DB_NAME = "db.sqlite3"
        DB_FILE = ROOT_DIR / DB_NAME
        data = DatabaseManager(DB_FILE)
        data.create_all_tables()
        data.save_db(cliente, conta, endereco, pessoa)

        print(f"Cliente {nome} adicionado com sucesso!")

    def login(self):
        print("\nLogin")

        identifier = input("Digite seu email ou CPF: ")
        senha = input("Digite sua senha: ")

        ROOT_DIR = Path(__file__).parent
        DB_NAME = "db.sqlite3"
        DB_FILE = ROOT_DIR / DB_NAME
        data = DatabaseManager(DB_FILE)
        
        client_id = data.get_client_id(identifier, senha)
        login = data.login(client_id)
        print(login)