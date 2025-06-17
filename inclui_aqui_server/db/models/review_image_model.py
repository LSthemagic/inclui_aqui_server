# inclui_aqui_server/db/models/establishment_image_model.py

import uuid
from datetime import datetime

from sqlalchemy import TEXT, Boolean, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inclui_aqui_server.db.database import table_registry  # Importa o table_registry


# Modelo ORM para a tabela 'establishment_images'
@table_registry.mapped_as_dataclass
class EstablishmentImage:
    __tablename__ = 'establishment_images'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, init=False
    )
    establishment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('establishments.id', ondelete='CASCADE'),
        nullable=False,
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), default=None
    )
    s3_url: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(TEXT, default=None)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    uploaded_at: Mapped[datetime] = mapped_column(default=func.now(), init=False)

    # Relações com outros modelos (importação diferida)
    establishment: Mapped['Establishment'] = relationship(backref='images')
    user: Mapped['User'] = relationship(backref='uploaded_establishment_images')

    def __repr__(self):
        return f"<EstablishmentImage(id={self.id}, establishment_id='{self.establishment_id}', s3_url='{self.s3_url}')>"
