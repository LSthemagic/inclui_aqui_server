from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Importa a dependência que nos dá a sessão do banco
from inclui_aqui_server.db.database import get_db_session
# Importa a classe do serviço que queremos instanciar
from inclui_aqui_server.services.user import UserService

def get_user_service(db: AsyncSession = Depends(get_db_session)) -> UserService:
    """
    Função de dependência que cria e retorna uma instância de UserService.

    Esta função atua como uma "fábrica" para a classe UserService. Para cada
    requisição, o FastAPI irá:
    1. Resolver a dependência `get_db_session` para obter uma sessão de banco.
    2. Passar essa sessão para o construtor do `UserService`.
    3. Injetar a instância resultante do `UserService` no endpoint.

    :param db: Sessão do banco de dados injetada pelo `get_db_session`.
    :type db: AsyncSession
    :return: Uma instância do UserService pronta para uso.
    :rtype: UserService
    """
    return UserService(db)