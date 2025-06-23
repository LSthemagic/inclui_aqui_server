from typing import Any
from fastapi import status

class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: str,
        data: Any = None 
    ):
        self.status_code = status_code
        self.detail = detail
        self.data = data 
        super().__init__(self.detail)

     
# --- Exceções de Negócio Específicas e Reutilizáveis ---
class NotFoundError(AppException):
    """Levantada quando um recurso não é encontrado. (HTTP 404)"""
    def __init__(self, resource: str = "Resource", data: Any = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found.",
            data=data
        )

class AlreadyExistsError(AppException):
    """Levantada quando se tenta criar um recurso que já existe. (HTTP 409)"""
    def __init__(self, resource: str = "Resource", field: str = "identifier", data: Any = None):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} with this {field} already exists.",
            data=data
        )

class UnauthorizedError(AppException):
    """Levantada para falhas de autenticação ou permissão. (HTTP 401)"""
    def __init__(self, detail: str = "Could not validate credentials", data: Any = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            data=data
        )