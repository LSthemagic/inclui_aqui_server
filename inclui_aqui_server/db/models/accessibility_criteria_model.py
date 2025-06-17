# inclui_aqui_server/db/models/accessibility_criteria_model.py

import uuid
from datetime import datetime

from sqlalchemy import TEXT, Boolean, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Modelo ORM para a tabela 'accessibility_criteria'
@table_registry.mapped_as_dataclass
class AccessibilityCriteria:
    __tablename__ = "accessibility_criteria"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(TEXT, default=None)
    category: Mapped[str | None] = mapped_column(String(50), default=None)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), init=False
    )

    def __repr__(self):
        return f"<AccessibilityCriteria(id={self.id}, name='{self.name}', category='{self.category}')>"
