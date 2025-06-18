from fastapi import APIRouter

from inclui_aqui_server.api.v1.endpoints import auth_user

# cria roteador principal
api_router_v1 = APIRouter()

# Inclui o router do endpoint no roteador principal
# Agora, todas as rotas de auth_user.router fazem parte de api_router_v1
api_router_v1.include_router(auth_user.router)
