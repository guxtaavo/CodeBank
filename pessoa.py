import re
from datetime import datetime

class Pessoa:
    def __init__(self, nome: str, documento: str,
                  data_nascimento: str) -> None:
        self.nome = nome
        if Pessoa._validar_cpf(documento):
            self.documento = documento
        else:
            raise ValueError("CPF inválido")
        if Pessoa._validar_data_nascimento(data_nascimento):
            self.data_nascimento = data_nascimento
        else:
            raise ValueError("Data de nascimento inválida")

    @staticmethod
    def _validar_cpf(documento) -> bool:
        cpf = documento
        
        # Remover caracteres não numéricos
        cpf = re.sub(r'\D', '', cpf)

        # Verificar se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return False

        # Verificar se todos os dígitos são iguais (ex: 111.111.111-11)
        if cpf == cpf[0] * len(cpf):
            return False

        # Cálculo do primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        primeiro_digito = (soma * 10 % 11) % 10

        # Cálculo do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        segundo_digito = (soma * 10 % 11) % 10

        # Verificar se os dígitos verificadores estão corretos
        return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"
    
    @staticmethod
    def _validar_data_nascimento(data_nascimento: str) -> bool:
        """
        Valida se a data de nascimento está no formato DD/MM/YYYY
        e se a pessoa tem pelo menos 18 anos.
        
        Args:
        data_nascimento (str): A data de nascimento no formato DD/MM/YYYY.
        
        Returns:
        bool: True se a data é válida e a pessoa tem pelo menos 18 anos,
          False caso contrário.
        """
        # Expressão regular para o formato DD/MM/YYYY
        regex = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(\d{4})$'
        
        # Verificar se a data está no formato correto
        if not re.fullmatch(regex, data_nascimento):
            return False
        
        try:
            # Converter a string para um objeto datetime
            data_nasc = datetime.strptime(data_nascimento, '%d/%m/%Y')
        except ValueError:
            # Data inválida (exemplo: 30/02/2023)
            return False
        
        # Calcular a idade
        hoje = datetime.now()
        idade = hoje.year - data_nasc.year - \
        ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        
        # Verificar se a idade é de pelo menos 18 anos
        return idade >= 18

    def __str__(self) -> str:
        return f'{self.nome} | {self.documento}'

    
if __name__ == "__main__":
    ...