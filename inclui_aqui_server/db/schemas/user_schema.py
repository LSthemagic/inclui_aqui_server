import enum
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# É uma boa prática redefinir o ENUM no arquivo de schema para
# desacoplar os schemas dos modelos do banco de dados.
class UserRole(str, enum.Enum):
    client = 'client'
    merchant = 'merchant'
    admin = 'admin'
    moderator = 'moderator'


# --- Schema Base ---
# Contém os campos compartilhados. Não é usado diretamente na API.
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    points: int = 0
    profile_image_url: Optional[str] = None
    preferences_json: Optional[dict] = None


# --- Schema para Criação ---
# Usado como o corpo da requisição para criar um usuário (POST).
# A senha é recebida aqui, mas nunca será retornada na resposta da API.
class UserCreate(UserBase):
    password: str


# --- Schema para Atualização ---
# Usado para atualizar um usuário (PUT/PATCH).
# Todos os campos são opcionais para permitir atualizações parciais.
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    points: Optional[int] = None
    profile_image_url: Optional[str] = None
    preferences_json: Optional[dict] = None


# --- Schema para Leitura/Retorno ---
# Este é o schema usado nas respostas da API (GET).
# Ele inclui campos gerados pelo banco de dados (id, created_at)
# e exclui campos sensíveis (hashed_password).
class UserRead(UserBase):
    # O ConfigDict com from_attributes=True permite que o Pydantic
    # leia os dados de um objeto de modelo SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# --- Schema Interno (Opcional) ---
# Representa o usuário completo como está no banco de dados.
# Útil para lógica interna, mas não deve ser retornado pela API.
class UserInDB(UserRead):
    hashed_password: str