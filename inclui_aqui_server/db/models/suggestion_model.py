# inclui_aqui_server/db/models/suggestion_model.py

import uuid
from datetime import datetime

from sqlalchemy import TEXT, Boolean, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Modelo ORM para a tabela 'suggestions'
@table_registry.mapped_as_dataclass
class Suggestion:
    __tablename__ = "suggestions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    establishment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("establishments.id", ondelete="CASCADE"),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(TEXT, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    ai_model_version: Mapped[str | None] = mapped_column(String(50), default=None)
    source_review_ids: Mapped[list[uuid.UUID] | None] = mapped_column(
        ARRAY(UUID(as_uuid=True)), default=None
    )

    # Relação com o modelo Establishment (importação diferida)
    establishment: Mapped["Establishment"] = relationship(backref="suggestions")

    def __repr__(self):
        return f"<Suggestion(id={self.id}, establishment_id='{self.establishment_id}', is_read={self.is_read})>"
