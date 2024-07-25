from pessoa import Pessoa
from cliente import Cliente
from conta import Conta
from endereco import Endereco
from data import DatabaseManager
from pathlib import Path
import sys
import os
from acoes_conta import AcoesConta

class Menu:
    def __init__(self):
        ROOT_DIR = Path(__file__).parent
        DB_NAME = "db.sqlite3"
        self.DB_FILE = ROOT_DIR / DB_NAME
        self.data = DatabaseManager(self.DB_FILE)
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
        conta = Conta(email, senha, None, None, None)
        cliente = Cliente(pessoa, endereco, conta)

        self.data.create_all_tables()
        self.data.save_db(cliente, conta, endereco, pessoa)

        print(f"Cliente {nome} adicionado com sucesso!")

    def login(self):
        print("\nLogin")

        identifier = input("Digite seu CPF: ")
        senha = input("Digite sua senha: ")
        identifier_formated = Pessoa._formatar_cpf(identifier)

        client_id = self.data.get_client_login(identifier_formated, senha)
        login = self.data.login(client_id)
        endereco = Endereco(login[1][0])
        pessoa = Pessoa(login[3][1], login[3][0], login[3][2])
        conta = Conta(login[0][1], login[2][0], login[2][2],
                      login[0][2], login[2][1])
        cliente = Cliente(pessoa, endereco, conta)
        self.menu_cliente(cliente)

    def menu_cliente(self, cliente: Cliente):
        os.system('cls')
        while True:
            print('-'*25)
            print(f'Seja bem-vindx, {cliente.pessoa.nome}!')
            print('-'*25)
            print('Opções:')
            print('1- Consultar saldo')
            print('2- Consultar extrato')
            print('3- Realizar transferência')
            print('4- Realizar depósito (QRCode)')
            print('5- Sair')
            choice = input("Escolha uma opção: ")
            if choice == '1':
                os.system('cls')
                print(f'O seu saldo é de: R${cliente.conta.get_saldo():.2f}')
            elif choice == '2':
                os.system('cls')
                print('Lógica de puxar o extrato no DB.')
            elif choice == '3':
                os.system('cls')
                cpf_destinatario = input('Digite o CPF da pessoa para realizar a transação: ')
                valor_da_transacao = float(input('Digite o valor que você deseja transferir: '))
                AcoesConta.transferir(cliente, valor_da_transacao, cpf_destinatario)
            elif choice == '4':
                os.system('cls')
                valor_da_transacao = float(input('Digite o valor que você deseja depositar: '))
                cliente.conta.depositar(valor_da_transacao)
                self.data.update_account(cliente.conta)
            elif choice == '5':
                os.system('cls')
                self.data.update_client(cliente)
                self.data.update_account(cliente.conta)
                print('Saindo do CodeBank, volte sempre!')
                sys.exit()
            else:
                print('Opção inválida, tente novamente.')
