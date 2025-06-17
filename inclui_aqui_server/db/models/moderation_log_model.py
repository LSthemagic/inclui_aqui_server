# inclui_aqui_server/db/models/moderation_log_model.py

import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, TEXT, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Definição do ENUM moderation_content_type
class ModerationContentType(enum.Enum):
    review = 'review'
    comment = 'comment'
    establishment_image = 'establishment_image'
    review_image = 'review_image'
    establishment = 'establishment'


# Definição do ENUM moderation_action
class ModerationAction(enum.Enum):
    approve = 'approve'
    reject = 'reject'
    delete = 'delete'
    warn_user = 'warn_user'
    edit = 'edit'


# Modelo ORM para a tabela 'moderation_logs'
@table_registry.mapped_as_dataclass
class ModerationLog:
    __tablename__ = 'moderation_logs'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    moderator_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    content_type: Mapped[ModerationContentType] = mapped_column(
        Enum(ModerationContentType, name='moderation_content_type'), nullable=False
    )
    content_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    action: Mapped[ModerationAction] = mapped_column(
        Enum(ModerationAction, name='moderation_action'), nullable=False
    )
    reason: Mapped[str | None] = mapped_column(TEXT, default=None)
    action_details: Mapped[dict | None] = mapped_column(JSON, default=None)
    action_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)

    # Relação com o modelo User (moderador) (importação diferida)
    moderator: Mapped['User'] = relationship(backref='moderation_actions')

    def __repr__(self):
        return f"<ModerationLog(id={self.id}, moderator_id='{self.moderator_id}', action='{self.action.value}', content_type='{self.content_type.value}', content_id='{self.content_id}')>"
