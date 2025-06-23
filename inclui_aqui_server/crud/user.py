import uuid
from typing import Optional, Dict, Any, Union

from sqlalchemy.orm import Session
from inclui_aqui_server.db.models import User
from inclui_aqui_server.db.schemas.user_schema import UserCreate, UserUpdate

class UserCRUD:
    """
    Classe de Ações CRUD para o modelo User.
    Encapsula toda a lógica de acesso ao banco de dados para os usuários.
    """
    
    def get(self, db: Session, user_id: uuid.UUID) -> Optional[User]:
        """
        Busca um único usuário pelo seu ID.

        :param db: A sessão do banco de dados.
        :param user_id: O UUID do usuário.
        :return: O objeto User ou None se não for encontrado.
        """
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Busca um usuário pelo seu email.

        :param db: A sessão do banco de dados.
        :param email: O email do usuário.
        :return: O objeto User ou None se não for encontrado.
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        Busca um único usuário pelo seu nome de usuário.

        :param db: A sessão do banco de dados.
        :param username: O nome de usuário.
        :return: O objeto User ou None se não for encontrado.
        """
        return db.query(User).filter(User.username == username).first()
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Busca múltiplos usuários com paginação.

        :param db: A sessão do banco de dados.
        :param skip: O número de registros a pular.
        :param limit: O número máximo de registros a retornar.
        :return: Uma lista de objetos User.
        """
        return db.query(User).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, user_in: UserCreate, hashed_password: str) -> User:
        """
        Cria um novo usuário no banco de dados.

        Nota: A responsabilidade de hashear a senha é da camada de serviço.
        Esta função recebe a senha já hasheada.

        :param db: A sessão do banco de dados.
        :param user_in: O schema Pydantic com os dados de criação.
        :param hashed_password: A senha já processada (hash).
        :return: O objeto User recém-criado.
        """
        
        # converte o schema Pydantic para um dicionário
        user_data = user_in.model_dump()
        # remove o campo de senha, pois não deve ser armazenado
        # pop() retorna o valor removido e aceita um valor padrão (None) se a chave não existir
        # é mais seguro pois não gera KeyError se a chave não existir
        user_data.pop('password', None)
        
        # Cria a instância do modelo SQLAlchemy com a senha hasheada
        db_obj = User(**user_data, hashed_password=hashed_password)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)  # Atualiza o objeto com os dados do banco (ex: id, created_at)
        return db_obj
    
    def update(self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Atualiza um usuário existente no banco de dados.

        :param db: A sessão do banco de dados.
        :param db_obj: O objeto User atual a ser modificado.
        :param obj_in: Um schema Pydantic ou um dicionário com os campos a serem atualizados.
        :return: O objeto User atualizado.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # exclude_unset=True garante que apenas os campos enviados sejam atualizados
            update_data = obj_in.model_dump(exclude_unset=True)

        # Nota: Se 'password' estiver em update_data, a camada de serviço
        # já deve tê-lo hasheado e renomeado para 'hashed_password'.
        if "password" in update_data:
            hashed_password = ... # Lógica de hash deve vir da camada de serviço
            update_data["hashed_password"] = hashed_password
            del update_data["password"]

        # Atualiza os campos do objeto do banco de dados
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
       
    def remove(self, db: Session, *, user_id: uuid.UUID) -> Optional[User]:
        """
        Remove um usuário do banco de dados pelo seu ID.

        :param db: A sessão do banco de dados.
        :param user_id: O UUID do usuário a ser removido.
        :return: O objeto User que foi removido ou None se não encontrado.
        """
        # .get() é otimizado para busca por chave primária
        obj = db.query(User).get(user_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
# Cria uma instância única da classe CRUDUser para ser importada em outros lugares.
# Isso funciona como um singleton, garantindo que você use sempre a mesma instância.
user = UserCRUD()