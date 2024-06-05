from endereco import Endereco
from pessoa import Pessoa

class Cliente(Pessoa):
    def __init__(self, nome: str, endereco: Endereco, documento: str, 
                 pessoa: str) -> None:
        super().__init__(nome, endereco, documento)
        self.conta = self.cria_conta()


    def cria_conta(self):
        ...