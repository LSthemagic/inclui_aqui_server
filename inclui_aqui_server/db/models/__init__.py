# inclui_aqui_server/db/models/__init__.py

# Importar o table_registry para que os modelos possam usá-lo
from accessibility_criteria_model import AccessibilityCriteria
from ai_feedback_log_model import AIFeedbackLog, FeedbackType
from badge_model import Badge, UserBadge
from comment_model import Comment
from establishment_image_model import EstablishmentImage
from establishment_model import Establishment
from moderation_log_model import ModerationAction, ModerationContentType, ModerationLog
from review_image_model import ReviewImage
from review_model import Review
from suggestion_model import Suggestion

# Importar todos os modelos SQLAlchemy.
# A base `Base` não é mais explicitamente importada aqui, pois os modelos usam o `table_registry`.
from user_model import User, UserRole
from user_search_history_model import UserSearchHistory

from inclui_aqui_server.db.database import (  # Adicione async_engine aqui se for usar Base.metadata em app.py
    async_engine as async_engine,
)
from inclui_aqui_server.db.database import (
    table_registry,
)

# Opcional: Para facilitar o uso do Base.metadata para criação de tabelas (ex: no startup do FastAPI)
# A metadata é acessada através do table_registry.
Base = table_registry.generate_base()

__all__ = [
    'Base',  # Base para create_all
    'User',
    'UserRole',
    'Establishment',
    'Review',
    'Comment',
    'Badge',
    'UserBadge',
    'Suggestion',
    'AIFeedbackLog',
    'FeedbackType',
    'UserSearchHistory',
    'AccessibilityCriteria',
    'EstablishmentImage',
    'ReviewImage',
    'ModerationLog',
    'ModerationContentType',
    'ModerationAction',
]
