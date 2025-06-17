# inclui_aqui_server/db/models/badge_model.py

import uuid
from datetime import datetime

from sqlalchemy import TEXT, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Modelo ORM para a tabela 'badges'
@table_registry.mapped_as_dataclass
class Badge:
    __tablename__ = "badges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(255), default=None)

    def __repr__(self):
        return f"<Badge(id={self.id}, name='{self.name}')>"


# Modelo ORM para a tabela 'user_badges' (tabela de junção)
@table_registry.mapped_as_dataclass
class UserBadge:
    __tablename__ = "user_badges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    badge_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("badges.id", ondelete="CASCADE"), nullable=False
    )
    awarded_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)

    # Garante que um usuário não ganhe o mesmo badge múltiplas vezes
    __table_args__ = (UniqueConstraint("user_id", "badge_id", name="_user_badge_uc"),)

    # Relações com outros modelos (importação diferida)
    user: Mapped["User"] = relationship(backref="user_badges")
    badge: Mapped["Badge"] = relationship(backref="user_badges")

    def __repr__(self):
        return f"<UserBadge(id={self.id}, user_id='{self.user_id}', badge_id='{self.badge_id}')>"
