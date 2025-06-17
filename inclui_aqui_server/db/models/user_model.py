import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, Enum, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from inclui_aqui_server.db.database import table_registry


# Definição do ENUM user_role
class UserRole(enum.Enum):
    client = 'client'
    merchant = 'merchant'
    admin = 'admin'
    moderator = 'moderator'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name='user_role'), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), init=False
    )
    points: Mapped[int] = mapped_column(Integer, default=0)
    profile_image_url: Mapped[str | None] = mapped_column(String(255), default=None)
    preferences_json: Mapped[dict | None] = mapped_column(JSON, default=None)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
