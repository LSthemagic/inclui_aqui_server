from http import HTTPStatus
from fastapi import APIRouter, Depends, status
from inclui_aqui_server.db.schemas import GenericResponseModel
import uuid
from inclui_aqui_server.api.dependencies import get_user_service
from inclui_aqui_server.services.user import UserService
from inclui_aqui_server.db.schemas.user_schema import UserRead, UserCreate


router = APIRouter(
    tags=['Authentication']  # Agrupa na documentação /docs
)


@router.get('/auth/status', response_model=GenericResponseModel)
def get_auth_status():
    """
    Endpoint de teste para verificar o status do módulo de autenticação.
    """
    return GenericResponseModel(
        message='Auth module is running',
        status=HTTPStatus.OK,
        data={'version': 'v1'},
    )

router = APIRouter()

@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário"
)
async def create_new_user(
    user_in: UserCreate,
    # O endpoint agora depende diretamente do serviço.
    user_service: UserService = Depends(get_user_service)
):
    """
    Cria um novo usuário.

    A lógica de negócio e as exceções são tratadas na camada de serviço.
    O handler de exceção global cuidará de transformar exceções em respostas HTTP.
    
    :param user_in: Os dados do novo usuário.
    :type user_in: CreateUserSchema
    :param user_service: Instância do serviço de usuário injetada.
    :type user_service: UserService
    :return: Os dados do usuário recém-criado.
    :rtype: UserReadSchema
    """
    # A chamada ao método do serviço agora precisa de 'await'
    created_user = await user_service.create_user(user_in)
    return created_user

@router.get("/{user_id}", response_model=UserRead, summary="Busca um usuário por ID")
async def get_user_by_id(
    user_id: uuid.UUID,
    user_service: UserService = Depends(get_user_service)
):
    """
    Busca e retorna um único usuário pelo seu ID.

    Se o usuário não for encontrado, o serviço levantará uma exceção `NotFoundError`,
    que será capturada pelo handler global e retornará um erro HTTP 404.

    :param user_id: O ID do usuário a ser buscado.
    :type user_id: uuid.UUID
    :param user_service: Instância do serviço de usuário injetada.
    :type user_service: UserService
    :return: Os dados do usuário encontrado.
    :rtype: UserReadSchema
    """
    user = await user_service.get_user(user_id)
    return user