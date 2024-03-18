from pydantic import BaseModel


class TokenModel(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserModel(BaseModel):

    username: str
    email: str
    full_name: str
    active: bool = True
    role: str = "user"

class CreateUserModel(UserModel):
    password: str

class ResponseUser(UserModel):
    id:str