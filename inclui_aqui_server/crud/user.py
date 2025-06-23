import uuid
from typing import Any, Dict, List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from inclui_aqui_server.db.models import User
from inclui_aqui_server.db.schemas.user_schema import UserCreate, UserUpdate
from sqlalchemy import select

class UserCRUD:
    """
    Classe de Ações CRUD para o modelo User.
    Encapsula toda a lógica de acesso ao banco de dados para os usuários.
    """

    async def get(self, db: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        """
        Busca um único usuário pelo seu ID.

        :param db: A sessão do banco de dados assíncrona.
        :param user_id: O UUID do usuário.
        :return: O objeto User ou None se não for encontrado.
        """
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        Busca um usuário pelo seu email.

        :param db: A sessão do banco de dados assíncrona.
        :param email: O email do usuário.
        :return: O objeto User ou None se não for encontrado.
        """
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """
        Busca um único usuário pelo seu nome de usuário.

        :param db: A sessão do banco de dados assíncrona.
        :param username: O nome de usuário.
        :return: O objeto User ou None se não for encontrado.
        """
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Busca múltiplos usuários com paginação.

        :param db: A sessão do banco de dados assíncrona.
        :param skip: O número de registros a pular.
        :param limit: O número máximo de registros a retornar.
        :return: Uma lista de objetos User.
        """
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, user_in: UserCreate, hashed_password: str) -> User:
        """
        Cria um novo usuário no banco de dados.

        Nota: A responsabilidade de hashear a senha é da camada de serviço.
        Esta função recebe a senha já hasheada.

        :param db: A sessão do banco de dados assíncrona.
        :param user_in: O schema Pydantic com os dados de criação.
        :param hashed_password: A senha já processada (hash).
        :return: O objeto User recém-criado.
        """
        # Converte o schema Pydantic para um dicionário
        user_data = user_in.model_dump()
        # Remove o campo de senha, pois não deve ser armazenado.
        # pop() é mais seguro pois não gera KeyError se a chave não existir.
        user_data.pop('password', None)

        # Cria a instância do modelo SQLAlchemy com a senha hasheada
        db_obj = User(**user_data, hashed_password=hashed_password)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)  # Atualiza o objeto com os dados do banco (ex: id, created_at)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Atualiza um usuário existente no banco de dados.

        Nota: A camada de serviço é responsável por preparar o dicionário `obj_in`,
        incluindo o hashing de uma nova senha, se aplicável.

        :param db: A sessão do banco de dados assíncrona.
        :param db_obj: O objeto User atual a ser modificado.
        :param obj_in: Um schema Pydantic ou um dicionário com os campos a serem atualizados.
        :return: O objeto User atualizado.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # exclude_unset=True garante que apenas os campos enviados sejam atualizados
            update_data = obj_in.model_dump(exclude_unset=True)

        # Atualiza os campos do objeto do banco de dados
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, user_id: uuid.UUID) -> Optional[User]:
        """
        Remove um usuário do banco de dados pelo seu ID.

        :param db: A sessão do banco de dados assíncrona.
        :param user_id: O UUID do usuário a ser removido.
        :return: O objeto User que foi removido ou None se não encontrado.
        """
        # Reutiliza o método get assíncrono para encontrar o objeto
        obj = await self.get(db, user_id=user_id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj

# Cria uma instância única da classe CRUDUser para ser importada em outros lugares.
# Isso funciona como um singleton, garantindo que você use sempre a mesma instância.
user_crud = UserCRUD()