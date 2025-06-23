
from passlib.context import CryptContext

class PasswordHandler:
    """
    Classe para manipulação de senhas, incluindo criptografia e verificação.
    """
    def __init__(self):
        """
        Inicializa o contexto de criptografia.
        """
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha em texto simples corresponde à senha criptografada.
        
        :param plain_password: Senha em texto simples.
        :param hashed_password: Senha criptografada.
        :return: True se as senhas corresponderem, False caso contrário.
        """
        return self._pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """
        Criptografa a senha em texto simples.
        
        :param password: Senha em texto simples.
        :return: Senha criptografada.
        """
        return self._pwd_context.hash(password)

password_handler = PasswordHandler()