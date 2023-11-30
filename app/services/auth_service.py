import http

from fastapi.responses import RedirectResponse
from app.services.ong_service import OngService
from app.services.adopter_service import AdopterService
from fastapi import HTTPException, Response
from app.domain.models.ong import OngModel
from app.domain.models.adopter import AdopterModel
from app.domain.models.dto.response import ResponseDTO


class AuthService:
    def __init__(self):
        self.ong_service = OngService()
        self.adopter_service = AdopterService()

    def authenticate(self, user: str, password: str):
        if len(user) == 14:
            entitie = self.ong_service.get_ong_by_cnpj(user)
            model = OngModel()
        elif len(user) == 11:
            entitie = self.adopter_service.get_adopter_by_cpf(user)
            model = AdopterModel()
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid user (not a CNPJ or CPF)"
            )
        print(entitie, flush=True)

        if entitie is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid user or password"
            )
        if entitie["password"] != password:
            raise HTTPException(
                status_code=401,
                detail="Invalid user or password"
            )

        return model.helper(entitie)