from fastapi import FastAPI
from http import HTTPStatus
from inclui_aqui_server.core.config import settings
from inclui_aqui_server.api.v1.api import api_router_v1
from inclui_aqui_server.db.schemas import ResponseModel

app = FastAPI(title=settings.PROJECT_NAME)

# 1. Define a lista de servidores (Base URL) para a documentação
#Isso cria um menu dropdown na sua documentação para escolher o ambiente.
servers = [
    {
        "url": "https://api.incluiaqui.com", # URL do seu servidor de produção
        "description": "Ambiente de Produção (Production)"
    },
    {
        "url": "http://127.0.0.1:8000", # URL do seu servidor local
        "description": "Ambiente de Desenvolvimento (Local)"
    },
]

# 2. Crie a instância do FastAPI com os novos parâmetros
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    servers=servers,
    root_path=settings.API_V1_STR
)

# Inclui todas as rotas da V1 na aplicação
app.include_router(api_router_v1)


@app.get('/', response_model=ResponseModel)
def health_check():
    
    return ResponseModel(
        message='Root module is running',
        status=HTTPStatus.OK,
        data={'version': 'v1'},
    )   