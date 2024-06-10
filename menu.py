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
            print("2. Sair")
            choice = input("Escolha uma opção: ")

            if choice == '1':
                self.add_new_client()
            elif choice == '2':
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
        conta = Conta(email, senha)
        cliente = Cliente(pessoa, endereco, conta)

        ROOT_DIR = Path(__file__).parent
        DB_NAME = "db.sqlite3"
        DB_FILE = ROOT_DIR / DB_NAME
        data = DatabaseManager(DB_FILE)
        data.create_all_tables()
        data.save_db(cliente, conta, endereco, pessoa)

        print(f"Cliente {nome} adicionado com sucesso!")

# from pessoa import Pessoa
# from cliente import Cliente
# from conta import Conta
# from endereco import Endereco
# from data import DatabaseManager
# from pathlib import Path

# class Menu():
#     def __init__(self) -> None:
#         Menu.sla()
    
#     @staticmethod
#     def sla():
#         pessoa = Pessoa('Gustavo', '649.238.530-69', '23/06/2002')
#         endereco = Endereco('05407002')
#         conta = Conta('gustavo@gmail.com', '1234567#G')
#         cliente = Cliente(pessoa, endereco, conta)
#         ROOT_DIR = Path(__file__).parent
#         DB_NAME = "db.sqlite3"
#         DB_FILE = ROOT_DIR / DB_NAME
#         data = DatabaseManager(DB_FILE)
#         data.create_all_tables()
#         print(cliente.conta.data_criacao)
#         data.save_db(cliente, conta, endereco, pessoa)
#         # print(data)