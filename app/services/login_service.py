import http
from typing import Union

from fastapi.responses import RedirectResponse
from app.services.ong_service import OngService
from app.services.adopter_service import AdopterService
from fastapi import HTTPException, Response
from app.domain.models.ong import OngModel
from app.domain.models.adopter import AdopterModel
from app.domain.models.dto.response import ResponseDTO


class LoginService:
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

    # TODO: Apagar depois de ter os testes, não é mais necessário
    # Nova solução Com REDIRECT
    # def register(self, model: Union[OngModel, AdopterModel]) -> Response :
    #     if "cnpj" in model.model_dump():
    #         if len(model.model_dump().get("cnpj")) != 14:
    #             raise HTTPException(
    #                 status_code=400,
    #                 detail="Invalid CNPJ"
    #             )
    #         response = self.ong_service.create_ong(model)

    #     elif "cpf" in model.model_dump():
    #         if len(model.model_dump().get("cpf")) != 11:
    #             raise HTTPException(
    #                 status_code=400,
    #                 detail="Invalid CPF"
    #             )
    #         response = self.adopter_service.create_adopter(model)

    #     else:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Failed to register user"
    #         )

    #     if response.status != http.HTTPStatus.CREATED:
    #         return ResponseDTO(None, "Failed to register user", http.HTTPStatus.BAD_REQUEST)
    #     else:
    #         return ResponseDTO(None, "User registered successfully", http.HTTPStatus.CREATED)

    def get_user(self, id: str, roles: dict) -> ResponseDTO:
        if "ong" in roles:
            response = self.ong_service.get_ong_by_id(id)
            if response.status == http.HTTPStatus.OK:
                return ResponseDTO({"type": 1, "user": response.data}, "User retrieved successfully", http.HTTPStatus.OK)
            return ResponseDTO(None, "Wrong ong id", http.HTTPStatus.BAD_REQUEST)
        elif "user" in roles:
            response = self.adopter_service.get_adopter_by_id(id)
            if response.status == http.HTTPStatus.OK:
                return ResponseDTO({"type": 2, "user": response.data}, "User retrieved successfully", http.HTTPStatus.OK)
            return ResponseDTO(None, "Wrong user id", http.HTTPStatus.BAD_REQUEST)
        else:
            return ResponseDTO(None, "Invalid user", http.HTTPStatus.BAD_REQUEST)
        
        return ResponseDTO(None, "Failed to get user", http.HTTPStatus.BAD_REQUEST)