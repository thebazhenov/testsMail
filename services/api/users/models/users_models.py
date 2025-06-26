from pydantic import BaseModel

class UserModel(BaseModel):
    login: str
    email: str