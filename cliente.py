from pessoa import Pessoa
from endereco import Endereco
from conta import Conta

class Cliente():
    def __init__(self, pessoa: Pessoa, endereco: Endereco, conta: Conta) -> None:
        self.pessoa = pessoa
        self.endereco = endereco
        self.conta = conta
        
    def depositar(self, valor) -> None:
        if valor >= 0:
            self.conta.depositar(valor)

    def __str__(self) -> str:
        return f'{self.pessoa} | {self.endereco} | {self.conta}'