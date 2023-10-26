from app.domain.database.db import Database
from app.services.ong_service import OngService

class LoginService:
    def __init__(self):
        self.ong_service = OngService()

    def authenticate(self, cnpj: str, password: str): 
        ong = self.ong_service.get_ong_by_cnpj(cnpj)
        # TODO: tratar erros
        if ong is None:
            return None
        if ong["password"] != password:
            return None
        return ong