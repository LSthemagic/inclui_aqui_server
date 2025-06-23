import uuid
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

# Importa as camadas que o serviço irá orquestrar
from inclui_aqui_server.crud import user as user_crud
from inclui_aqui_server.core.security import password_handler
from inclui_aqui_server.db.schemas import UserCreate, UserUpdate
from inclui_aqui_server.db.models import User
from inclui_aqui_server.core.exception import NotFoundError, AlreadyExistsError

class UserService:
    def __init__(self, db: AsyncSession):
        """
        O serviço é inicializado com uma sessão de banco de dados assíncrona.

        :param db: A sessão do banco de dados a ser usada pelo serviço.
        :type db: AsyncSession
        """
        self.db = db

    async def get_user(self, user_id: uuid.UUID) -> User:
        """
        Busca um único usuário pelo seu ID de forma assíncrona.

        :param user_id: O ID do usuário a ser buscado.
        :type user_id: uuid.UUID
        :raises NotFoundError: Se o usuário com o ID especificado não for encontrado.
        :return: O objeto de modelo User correspondente.
        :rtype: User
        """
        db_user = await user_crud.get(self.db, user_id=user_id)
        if not db_user:
            raise NotFoundError(resource="User")
        return db_user

    async def get_users(self, skip: int, limit: int) -> List[User]:
        """
        Busca uma lista de usuários com paginação de forma assíncrona.

        :param skip: O número de registros a pular.
        :type skip: int
        :param limit: O número máximo de registros a retornar.
        :type limit: int
        :return: Uma lista de objetos de modelo User.
        :rtype: List[User]
        """
        return await user_crud.get_multi(self.db, skip=skip, limit=limit)

    async def create_user(self, user_in: UserCreate) -> User:
        """
        Cria um novo usuário, aplicando regras de negócio e hashing de senha.

        :param user_in: Os dados do usuário a ser criado, validados pelo schema.
        :type user_in: CreateUserSchema
        :raises AlreadyExistsError: Se um usuário com o mesmo e-mail já existir.
        :return: O objeto de modelo User recém-criado.
        :rtype: User
        """
        existing_user = await user_crud.get_by_email(self.db, email=user_in.email)
        if existing_user:
            raise AlreadyExistsError(resource="User", field="email")

        hashed_password = password_handler.get_password_hash(user_in.password)

        created_user = await user_crud.create(
            self.db,
            user_in=user_in,
            hashed_password=hashed_password
        )
        return created_user

    async def update_user(self, user_id: uuid.UUID, user_in: UserUpdate) -> User:
        """
        Atualiza um usuário existente de forma assíncrona.

        :param user_id: O ID do usuário a ser atualizado.
        :type user_id: uuid.UUID
        :param user_in: Os dados a serem atualizados.
        :type user_in: UpdateUserSchema
        :raises NotFoundError: Se o usuário a ser atualizado não for encontrado.
        :raises AlreadyExistsError: Se a atualização tentar usar um e-mail que já pertence a outro usuário.
        :return: O objeto de modelo User atualizado.
        :rtype: User
        """
        db_user = await self.get_user(user_id) # Reutiliza o método da própria classe
        update_data = user_in.model_dump(exclude_unset=True)
        
        # Regra de negócio: se o e-mail estiver sendo atualizado, verificar duplicidade
        if "email" in update_data and update_data["email"] != db_user.email:
            existing_user = await user_crud.get_by_email(self.db, email=update_data["email"])
            if existing_user:
                raise AlreadyExistsError(resource="User", field="email")
        
        # Regra de negócio: se a senha estiver sendo atualizada, gerar novo hash
        if "password" in update_data and update_data["password"]:
            hashed_password = password_handler.get_password_hash(update_data["password"])
            update_data["hashed_password"] = hashed_password
            del update_data["password"]

        return await user_crud.update(self.db, db_obj=db_user, obj_in=update_data)

    async def delete_user(self, user_id: uuid.UUID) -> User:
        """
        Deleta um usuário de forma assíncrona.

        :param user_id: O ID do usuário a ser deletado.
        :type user_id: uuid.UUID
        :raises NotFoundError: Se o usuário a ser deletado não for encontrado.
        :return: O objeto de modelo User que foi deletado.
        :rtype: User
        """
        db_user = await self.get_user(user_id)
        return await user_crud.remove(self.db, user_id=db_user.id)