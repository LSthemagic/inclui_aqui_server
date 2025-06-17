from pydantic import BaseModel


class ResponseModel(BaseModel):
    status: str
    message: str
    data: dict = None
