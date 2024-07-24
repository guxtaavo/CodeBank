import sqlite3
from cliente import Cliente
from pessoa import Pessoa
from endereco import Endereco
from conta import Conta
from pathlib import Path

class DatabaseManager:
    def __init__(self, path: Path):
        self.path = path

    # Criar todas as tabelas
    def create_all_tables(self):
        self._create_table_person()
        self._create_table_address()
        self._create_table_client()
        self._create_table_account()

    # Criar a tabela Pessoas
    def _create_table_person(self):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                data_nascimento TEXT NOT NULL
            )
            """
        )
        con.commit()
        con.close()

    # Criar a tabela Enderecos
    def _create_table_address(self):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Enderecos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rua TEXT NOT NULL,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                cep TEXT NOT NULL
            )
            """
        )
        con.commit()
        con.close()

    # Criar a tabela Clientes
    def _create_table_client(self):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cpf) REFERENCES Pessoas(cpf) ON DELETE CASCADE
            )
            """
        )
        con.commit()
        con.close()

    # Criar a tabela Contas
    def _create_table_account(self):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Contas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                senha TEXT NOT NULL,
                saldo REAL NOT NULL,
                usuario_id INTEGER NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES Clientes(id)
            )
            """
        )
        con.commit()
        con.close()

    # Método para resetar todo o banco de dados
    def _reset_database(self):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()

        try:
            # Desabilitar restrições de chaves estrangeiras
            cursor.execute("PRAGMA foreign_keys = OFF;")
            con.commit()

            # Obter todas as tabelas do banco de dados
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # Deletar todas as tabelas encontradas
            for table_name in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]};")

            con.commit()
            print("Banco de dados resetado com sucesso.")
        except Exception as e:
            print(f"Erro ao resetar o banco de dados: {e}")
        finally:
            con.close()

    def save_db(self, cliente: Cliente, conta: Conta,
                endereco: Endereco, pessoa: Pessoa):
        self._save_person(pessoa)
        self._save_address(endereco)
        self._save_client(cliente)
        self._save_account(conta)

    def _save_client(self, cliente: Cliente):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        TABLE_NAME = 'Clientes'
        sql = (
            f"INSERT INTO {TABLE_NAME} "
            "(cpf, email) "
            "VALUES "
            "(?, ?)"
        )
        cursor.execute(
            sql,
            [cliente.pessoa.documento, cliente.conta.email]
        )
        con.commit()
        con.close()

    def _save_account(self, conta: Conta):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        TABLE_NAME = 'Contas'
        sql = (
            f"INSERT INTO {TABLE_NAME} "
            "(senha, saldo, usuario_id) "
            "VALUES "
            "(?, ?, ?)"
        )
        cursor.execute(
            sql,
            [conta._senha, conta._saldo, conta.id_conta]
        )
        con.commit()
        con.close()

    def _save_address(self, endereco: Endereco):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        TABLE_NAME = 'Enderecos'
        sql = (
            f"INSERT INTO {TABLE_NAME} "
            "(rua, bairro, cidade, estado, cep) "
            "VALUES "
            "(?, ?, ?, ?, ?)"
        )
        cursor.execute(
            sql,
            [endereco.rua, endereco.bairro, endereco.cidade, endereco.estado,
              endereco.cep]
        )
        con.commit()
        con.close()

    def _save_person(self, pessoa: Pessoa):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        TABLE_NAME = 'Pessoas'
        sql = (
            f"INSERT INTO {TABLE_NAME} "
            "(cpf, nome, data_nascimento) "
            "VALUES "
            "(?, ?, ?)"
        )
        cursor.execute(
            sql,
            [pessoa.documento, pessoa.nome, pessoa.data_nascimento]
        )
        con.commit()
        con.close()

    def get_client_id(self, identifier: str, password: str) -> str | None:
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            SELECT id, cpf
            FROM Clientes
            WHERE cpf = ?
            """, (identifier,)
        )
        result = cursor.fetchone()
        print(result)
        con.close()
        return result[0]
    
    def login(self, id: str | None) -> list:
        get_client_data = self._get_client_data(id)
        get_client_addres = self._get_client_addrees(id)
        get_client_acc = self._get_client_account(id)
        get_person_data = self._get_person_data(id)
        return [get_client_data, get_client_addres, get_client_acc, 
                get_person_data]

    def _get_client_data(self, id):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            SELECT cpf, email, data_criacao
            FROM Clientes
            WHERE id = ?
            """, (id,)
        )
        result = cursor.fetchone()
        con.close()
        return result

    def _get_client_addrees(self, id):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            SELECT cep
            FROM Enderecos
            WHERE id = ?
            """, (id,)
        )
        result = cursor.fetchone()
        con.close()
        return result

    def _get_client_account(self, id):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            SELECT senha, saldo, usuario_id
            FROM Contas
            WHERE id = ?
            """, (id,)
        )
        result = cursor.fetchone()
        con.close()
        return result

    def _get_person_data(self, id):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            SELECT cpf, nome, data_nascimento
            FROM Pessoas
            WHERE id = ?
            """, (id,)
        )
        result = cursor.fetchone()
        con.close()
        return result