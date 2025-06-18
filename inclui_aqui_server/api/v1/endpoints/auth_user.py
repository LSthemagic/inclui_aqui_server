from http import HTTPStatus

from fastapi import APIRouter

from inclui_aqui_server.db.schemas import ResponseModel

router = APIRouter(
    tags=['Authentication']  # Agrupa na documentação /docs
)


@router.get('/auth/status', response_model=ResponseModel)
def get_auth_status():
    """
    Endpoint de teste para verificar o status do módulo de autenticação.
    """
    return ResponseModel(
        message='Auth module is running',
        status=HTTPStatus.OK,
        data={'version': 'v1'},
    )
