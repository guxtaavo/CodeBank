from endereco import Endereco

class Pessoa:
    def __init__(self, nome: str, endereco: Endereco, documento: str) -> None:
        self.nome = nome
        self.endereco = endereco
        self.documento = documento

if __name__ == "__main__":
    ...