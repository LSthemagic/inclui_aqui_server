from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from inclui_aqui_server.api.v1.api import api_router_v1
from inclui_aqui_server.core.config import settings
from inclui_aqui_server.db.schemas import GenericResponseModel, Status
from inclui_aqui_server.core.exception import AppException

app = FastAPI(title=settings.PROJECT_NAME)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """
    Captura todas as exceções que herdam de AppException e retorna
    uma resposta JSON padronizada com o status_code e detalhe da exceção.
    """
    # 1. Cria o corpo da resposta usando o nosso schema genérico
    response_body = GenericResponseModel(
        # Usa o Enum para garantir consistência
        status=Status.FAIL if 400 <= exc.status_code < 500 else Status.ERROR,
        message=exc.detail,
        data=exc.data
    )

    # 2. Retorna um objeto JSONResponse, que é o que o FastAPI espera.
    #    - status_code: Define o código de status HTTP real da resposta.
    #    - content: O corpo da resposta. Usamos .model_dump() para converter
    #      o objeto Pydantic em um dicionário serializável.
    return JSONResponse(
        status_code=exc.status_code,
        content=response_body.model_dump(exclude_none=True)
    )
#  Define a lista de servidores (Base URL) para a documentação
# Isso cria um menu dropdown na sua documentação para escolher o ambiente.
servers = [
    {
        'url': 'https://api.incluiaqui.com',  # URL do seu servidor de produção
        'description': 'Ambiente de Produção (Production)',
    },
    {
        'url': 'http://127.0.0.1:8000',  # URL do seu servidor local
        'description': 'Ambiente de Desenvolvimento (Local)',
    },
]

# 2. Crie a instância do FastAPI com os novos parâmetros
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    servers=servers,
    root_path=settings.API_V1_STR,
)

# Inclui todas as rotas da V1 na aplicação
app.include_router(api_router_v1)


@app.get('/', response_model=GenericResponseModel)
def health_check():
    return GenericResponseModel(
        message='Root module is running',
        status=HTTPStatus.OK,
        data={'version': 'v1'},
    )
