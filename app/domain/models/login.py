from pydantic import BaseModel

class LoginModel(BaseModel):
    user: str
    password: str
