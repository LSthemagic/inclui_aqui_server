# inclui_aqui_server/db/models/user_search_history_model.py

import uuid
from datetime import datetime

from sqlalchemy import JSON, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Modelo ORM para a tabela 'user_search_history'
@table_registry.mapped_as_dataclass
class UserSearchHistory:
    __tablename__ = "user_search_history"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    query: Mapped[str] = mapped_column(String(255), nullable=False)
    search_filters: Mapped[dict | None] = mapped_column(JSON, default=None)
    search_results_ids: Mapped[list[uuid.UUID] | None] = mapped_column(
        ARRAY(UUID(as_uuid=True)), default=None
    )
    timestamp: Mapped[datetime] = mapped_column(default=func.now(), init=False)

    # Relação com o modelo User (importação diferida)
    user: Mapped["User"] = relationship(backref="search_history")

    def __repr__(self):
        return f"<UserSearchHistory(id={self.id}, user_id='{self.user_id}', query='{self.query}')>"
