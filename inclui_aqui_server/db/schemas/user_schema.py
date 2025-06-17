from pydantic import BaseModel, EmailStr


class UserAuth(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    points: int
    profile_image_url: str | None


class AllUsersPublic(BaseModel):
    users: list[UserPublic]
