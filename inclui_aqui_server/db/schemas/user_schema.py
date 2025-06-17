from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    content: str


class UserModel(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr


class AllUsersPublic(BaseModel):
    users: list[UserPublic]
