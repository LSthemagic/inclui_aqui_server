# inclui_aqui_server/db/models/establishment_model.py

import uuid
from datetime import datetime

from sqlalchemy import DECIMAL, JSON, TEXT, Boolean, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Modelo ORM para a tabela 'establishments'
@table_registry.mapped_as_dataclass
class Establishment:
    __tablename__ = 'establishments'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(DECIMAL(10, 8), nullable=False)
    longitude: Mapped[float] = mapped_column(DECIMAL(11, 8), nullable=False)
    type: Mapped[str | None] = mapped_column(String(100), default=None)
    google_place_id: Mapped[str | None] = mapped_column(String(255), default=None)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='RESTRICT'), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), init=False
    )
    main_image_url: Mapped[str | None] = mapped_column(String(255), default=None)
    description: Mapped[str | None] = mapped_column(TEXT, default=None)
    accessibility_features_json: Mapped[dict | None] = mapped_column(JSON, default=None)

    # Relação com o modelo User (um estabelecimento pertence a um usuário)
    # Importação diferida para evitar dependência circular imediata
    owner: Mapped['User'] = relationship(backref='establishments')

    def __repr__(self):
        return f"<Establishment(id={self.id}, name='{self.name}', type='{self.type}')>"
