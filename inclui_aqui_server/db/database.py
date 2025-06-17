from core.config import Settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import registry

DATABASE_URL = Settings().DATABASE_URL

async_engine = create_async_engine(DATABASE_URL, echo=True)

# Cria o registry para mapear as classes para tabelas
table_registry = registry()

# Cria o motor de banco de dados assíncrono
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Cria um sessionmaker para sessões assíncronas
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


# Função para obter uma sessão de banco de dados por requisição (dependência do FastAPI)
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
