# inclui_aqui_server/db/models/comment_model.py

import uuid
from datetime import datetime

from sqlalchemy import TEXT, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Modelo ORM para a tabela 'comments'
@table_registry.mapped_as_dataclass
class Comment:
    __tablename__ = 'comments'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    review_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('reviews.id', ondelete='CASCADE'), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    content: Mapped[str] = mapped_column(TEXT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), init=False
    )

    # Relações com outros modelos (importação diferida)
    review: Mapped['Review'] = relationship(backref='comments')
    user: Mapped['User'] = relationship(backref='comments')

    def __repr__(self):
        return f"<Comment(id={self.id}, review_id='{self.review_id}', user_id='{self.user_id}')>"
