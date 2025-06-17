# inclui_aqui_server/db/models/review_model.py

import uuid
from datetime import datetime

from sqlalchemy import DECIMAL, JSON, TEXT, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Modelo ORM para a tabela 'reviews'
@table_registry.mapped_as_dataclass
class Review:
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    establishment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("establishments.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(TEXT, default=None)
    criteria_json: Mapped[dict | None] = mapped_column(JSON, default=None)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), init=False
    )
    image_urls: Mapped[list[str] | None] = mapped_column(ARRAY(String), default=None)
    sentiment_score: Mapped[float | None] = mapped_column(DECIMAL(3, 2), default=None)

    # Relações com outros modelos (importação diferida)
    establishment: Mapped["Establishment"] = relationship(backref="reviews")
    user: Mapped["User"] = relationship(backref="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, establishment_id='{self.establishment_id}', rating={self.rating})>"
