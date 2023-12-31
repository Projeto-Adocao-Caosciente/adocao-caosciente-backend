import http
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from app.domain.models.dto.response import ResponseDTO
from app.domain.models.login import LoginModel
from app.domain.models.ong import OngModel
from app.domain.models.adopter import AdopterModel
from app.services.auth_service import AuthService
from app.services.jwt_service import JWTBearer

router = APIRouter(
    prefix="/auth",
    tags=['authentication']
)

login_service = AuthService()
jwt_bearer = JWTBearer()

@router.post("/login")
async def token(
    login: LoginModel,
):
    user = login_service.authenticate(login.user, login.password)

    if "cnpj" in user and user["cnpj"]:
        role = "ong"
    elif "cpf" in user and user["cpf"]:
        role = "user"
    else:
        role = ""
        
    token = jwt_bearer.sign_jwt(user["id"], role)
    return ResponseDTO({"access_token": token}, "Login successfully", http.HTTPStatus.OK).dict()

@router.post("/refresh-token", dependencies=[Depends(jwt_bearer)])
async def refresh():
    token = jwt_bearer.refresh_jwt()
    return {"access_token": token}

@router.get("/profile", dependencies=[Depends(jwt_bearer)])
async def profile():
    roles = jwt_bearer.get_user_roles()
    if "ong" in roles:
        return RedirectResponse(url='/ong', status_code=http.HTTPStatus.TEMPORARY_REDIRECT)
    elif "user" in roles:
        return RedirectResponse(url='/adopter', status_code=http.HTTPStatus.TEMPORARY_REDIRECT)
    return ResponseDTO(None, "You don't have any role", http.HTTPStatus.UNAUTHORIZED).dict()

@router.post("/register_ong")
async def register_ong(ong: OngModel = Body(..., example=OngModel.Config.json_schema_extra)):
    return RedirectResponse(url='/ong', status_code=http.HTTPStatus.TEMPORARY_REDIRECT)

@router.post("/register_adopter")
async def register_adopter(adopter: AdopterModel = Body(..., example=AdopterModel.Config.json_schema_extra)):
    return RedirectResponse(url='/adopter', status_code=http.HTTPStatus.TEMPORARY_REDIRECT)