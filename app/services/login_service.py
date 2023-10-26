from app.services.ong_service import OngService
from fastapi import HTTPException

class LoginService:
    def __init__(self):
        self.ong_service = OngService()

    def authenticate(self, cnpj: str, password: str):
        ong = self.ong_service.get_ong_by_cnpj(cnpj)
        if ong is None:
            raise HTTPException(status_code=204, detail="Ong not found")
        if ong["password"] != password:
            raise HTTPException(status_code=401, detail="Invalid password")
        return ong

    def register(self, ong):
        return self.ong_service.create_ong(ong)