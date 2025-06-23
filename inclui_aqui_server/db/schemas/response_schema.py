from enum import Enum
from typing import Generic, TypeVar, Optional, List

from pydantic import BaseModel, ConfigDict


class Status(str, Enum):
    """Enum para os status padronizados da resposta da API."""
    SUCCESS = "success"
    FAIL = "fail"      # Para falhas de negócio (ex: e-mail já existe)
    ERROR = "error"    # Para erros inesperados do servidor (ex: exceção não tratada)


#TypeVar para representar o tipo de dado genérico
DataType = TypeVar("DataType")


#ResponseModel Genérico
class GenericResponseModel(BaseModel, Generic[DataType]):
    """
    Um modelo de resposta genérico para a API que fornece uma estrutura
    consistente e com tipagem para os dados de retorno.
    """
    # Garante que o modelo pode ser criado a partir de objetos de ORM (como SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

    status: Status
    message: Optional[str] = None
    data: Optional[DataType] = None