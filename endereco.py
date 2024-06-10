import requests

class Endereco():
    def __init__(self, cep: str) -> None:
        self.cep = None
        self.rua = None
        self.bairro = None
        self.cidade = None
        self.estado = None
        self._buscar_cep(cep)
        self._save_to_db()

    def _buscar_cep(self, cep):
        url = f'https://viacep.com.br/ws/{cep}/json/'
        try:
            r = requests.get(url)
            if r.status_code == 200:
                dados = r.json()
                self.cep = dados['cep']
                self.rua = dados['logradouro']
                self.bairro = dados['bairro']
                self.cidade = dados['localidade']
                self.estado = dados['uf']
            else:
                print(f'Erro ao encontrar o cep')
        except Exception as e:
            print(f'Erro inesperado: [{e}]')

    def _save_to_db(self):
        if self.rua is not None:
            ... # CRIAR A DB SE NAO EXISTIR
            ... # SAVE

    def __str__(self) -> str:
        return (
            f'{self.rua} | {self.bairro} | {self.cidade} | {self.estado}'
        )