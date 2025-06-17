# inclui_aqui_server/db/models/ai_feedback_log_model.py

import enum
import uuid
from datetime import datetime

from sqlalchemy import TEXT, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Definição do ENUM feedback_type
class FeedbackType(enum.Enum):
    useful = "useful"
    not_useful = "not_useful"
    irrelevant = "irrelevant"


# Modelo ORM para a tabela 'ai_feedback_logs'
@table_registry.mapped_as_dataclass
class AIFeedbackLog:
    __tablename__ = "ai_feedback_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    suggestion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("suggestions.id", ondelete="CASCADE"),
        nullable=False,
    )
    feedback_type: Mapped[FeedbackType] = mapped_column(
        Enum(FeedbackType, name="feedback_type"), nullable=False
    )
    feedback_comment: Mapped[str | None] = mapped_column(TEXT, default=None)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)

    # Relação com o modelo Suggestion (importação diferida)
    suggestion: Mapped["Suggestion"] = relationship(backref="feedback_logs")

    def __repr__(self):
        return f"<AIFeedbackLog(id={self.id}, suggestion_id='{self.suggestion_id}', type='{self.feedback_type.value}')>"
