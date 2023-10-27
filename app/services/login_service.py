from app.services.ong_service import OngService
from fastapi import HTTPException
from app.domain.models.ong import OngModel


class LoginService:
    def __init__(self):
        self.ong_service = OngService()

    def authenticate(self, user: str, password: str):
        ong = self.ong_service.get_ong_by_cnpj(user)
        if ong is None:
            raise HTTPException(
                status_code=401, detail="invalid user or password")
        if ong["password"] != password:
            raise HTTPException(
                status_code=401, detail="invalid user or password")
        return OngModel.ong_helper(ong)

    def register(self, ong: OngModel):
        # TODO: No futuro talvez tenha cadastro de adodante, voluntario, aqui é onde a lógica vai acontecer
        return self.ong_service.create_ong(ong)
