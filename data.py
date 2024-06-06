import sqlite3

class DatabaseManager:
    def __init__(self, path: str):
        self.path = path

    # Criar todas as tabelas
    def create_all_tables(self):
        self._create_table_person()
        self._create_table_address()
        self._create_table_clients()

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
                numero INTEGER NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                cep TEXT NOT NULL
            )
            """
        )
        con.commit()
        con.close()

    # Criar a tabela Clientes
    def _create_table_clients(self):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpf TEXT NOT NULL,
                endereco_id INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL,
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cpf) REFERENCES Pessoas(cpf) ON DELETE CASCADE,
                FOREIGN KEY (endereco_id) REFERENCES Enderecos(id) ON DELETE CASCADE
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