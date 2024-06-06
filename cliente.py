from pessoa import Pessoa
from endereco import Endereco
from datetime import datetime
import re
import uuid

class Cliente():
    def __init__(self, pessoa: Pessoa, endereco: Endereco, email: str,
                  senha: str) -> None:
        self.pessoa = pessoa
        self.endereco = endereco
        if Cliente._validar_email(email):
            self.email = email
        else:
            raise ValueError("Email inválido")
        if Cliente._validar_senha(senha):
            self.senha = senha
        else:
            raise ValueError("Senha inválida")
        self.conta = self._criar_id_conta()

    def _criar_id_conta(self) -> str | None:
        """_summary_

        Returns:
            str | None: _description_
        """
        try:
            # Verificar na DB se ja nao existe o mesmo ID
            return str(uuid.uuid4())
        except Exception as e:
            raise ValueError(f"Erro ao criar a conta: {e}")
    
    @staticmethod
    def _validar_senha(senha: str) -> bool:
        """
        Valida uma senha com os seguintes critérios:
        - Pelo menos 7 caracteres.
        - Pelo menos um número.
        - Pelo menos uma letra maiúscula.
        - Pelo menos um caractere especial.
        
        Args:
        senha (str): A senha a ser validada.
        
        Returns:
        bool: True se a senha for válida, False caso contrário.
        """
        # Verifica se a senha tem pelo menos 7 caracteres
        if len(senha) < 7:
            return False

        # Verifica se contém pelo menos um número
        if not re.search(r'\d', senha):
            return False

        # Verifica se contém pelo menos uma letra maiúscula
        if not re.search(r'[A-Z]', senha):
            return False

        # Verifica se contém pelo menos um caractere especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            return False

        # Se todas as verificações passaram, a senha é válida
        return True
    
    @staticmethod
    def _validar_email(email: str) -> bool:
        """
        Valida um endereço de e-mail usando uma expressão regular.
        
        Args:
        email (str): O e-mail a ser validado.
        
        Returns:
        bool: True se o e-mail for válido, False caso contrário.
        """
        # Expressão regular para validar o e-mail
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        # Usar re.fullmatch para garantir que a string completa corresponda
        # ao padrão
        if re.fullmatch(regex, email):
            return True
        else:
            return False
    
    def __str__(self) -> str:
        return f'{self.pessoa} | {self.endereco} | {self.conta}'