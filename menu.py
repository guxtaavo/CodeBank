from pessoa import Pessoa
from cliente import Cliente
from endereco import Endereco
from data import DatabaseManager
from pathlib import Path

class Menu():
    def __init__(self) -> None:
        Menu.sla()
    
    @staticmethod
    def sla():
        pessoa = Pessoa('Gustavo', '649.238.530-69', '23/06/2002')
        endereco = Endereco('05407002')
        cliente = Cliente(pessoa, endereco, 'gustavo@gmail.com', '1234567#G')
        ROOT_DIR = Path(__file__).parent
        DB_NAME = "db.sqlite3"
        DB_FILE = ROOT_DIR / DB_NAME
        data = DatabaseManager(DB_FILE)
        data.create_all_tables()
        print(cliente)
        # print(data)