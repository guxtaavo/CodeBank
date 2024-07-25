from pessoa import Pessoa
from data import DatabaseManager
from cliente import Cliente
from conta import Conta
from pathlib import Path
from endereco import Endereco

class AcoesConta():
    def __init__(self) -> None:
        pass
    
    @classmethod
    def transferir(cls, cliente: Cliente, valor: float, cpf: str) -> None:
        conta = cpf
        identifier_formated = Pessoa._formatar_cpf(conta)

        ROOT_DIR = Path(__file__).parent
        DB_NAME = "db.sqlite3"
        DB_FILE = ROOT_DIR / DB_NAME
        data = DatabaseManager(DB_FILE)
        
        client_id = data.get_client_id(identifier_formated)
        login = data.login(client_id)
        endereco = Endereco(login[1][0])
        pessoa = Pessoa(login[3][1], login[3][0], login[3][2])
        conta = Conta(login[0][1], login[2][0], login[2][2],
                      login[0][2], login[2][1])
        destinatario = Cliente(pessoa, endereco, conta)
        if cliente.conta.get_saldo() >= valor:
            cliente.conta._saldo -= valor
            destinatario.conta.depositar(valor)
            data.update_account(cliente.conta)
            data.update_account(destinatario.conta)
        else:
            raise ValueError("Saldo insuficiente para transferência")