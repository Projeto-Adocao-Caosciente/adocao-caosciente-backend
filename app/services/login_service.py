import http
from app.services.ong_service import OngService
from fastapi import HTTPException
from app.domain.models.ong import OngModel
from app.domain.models.dto.response import ResponseDTO


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

    def register(self, ong: OngModel) -> ResponseDTO:
        response = self.ong_service.create_ong(ong)

        if response.status != http.HTTPStatus.CREATED:
            return ResponseDTO(None, "failed to register ong", http.HTTPStatus.BAD_REQUEST)
        else:
            return ResponseDTO(None, "ong registered successfully", http.HTTPStatus.CREATED)