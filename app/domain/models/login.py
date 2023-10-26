from pydantic import BaseModel

class LoginModel(BaseModel):
    cnpj: str
    password: str
