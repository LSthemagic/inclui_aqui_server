import enum
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

# --- Enum para Papéis de Usuário ---
# Define os papéis possíveis para um usuário.
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
class UserCreate(UserBase):
    password: str


# --- Schema para Atualização ---
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    points: Optional[int] = None
    profile_image_url: Optional[str] = None
    preferences_json: Optional[dict] = None


# --- Schema para Leitura/Retorno ---
class UserRead(UserBase):
    # O ConfigDict com from_attributes=True permite que o Pydantic
    # leia os dados de um objeto de modelo SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# --- Schema Interno ---
class UserInDB(UserRead):
    hashed_password: str