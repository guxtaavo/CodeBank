import uuid
import re
from datetime import datetime

class Conta:
    def __init__(self, email: str, senha: str, id_conta: int | None,
                  data_criacao: str | None, saldo: float | None) -> None:
        self._saldo = saldo if saldo is not None else 0
        if Conta._validar_email(email):
            self.email = email
        else:
            raise ValueError("Email inválido")
        if Conta._validar_senha(senha):
            self._senha = senha
        else:
            raise ValueError("Senha inválida")
        self.id_conta = id_conta if id_conta is not None\
            else self._criar_id_conta()
        self.data_criacao = data_criacao if data_criacao is not None\
              else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
        if not re.search(r"\d", senha):
            return False

        # Verifica se contém pelo menos uma letra maiúscula
        if not re.search(r"[A-Z]", senha):
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
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        # Usar re.fullmatch para garantir que a string completa corresponda
        # ao padrão
        if re.fullmatch(regex, email):
            return True
        else:
            return False

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

    def depositar(self, valor) -> None:
        self._saldo += valor

    def get_saldo(self) -> float:
        return self._saldo

    def __str__(self) -> str:
        return f'{self.id_conta}'
