import http
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse, RedirectResponse
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
    role = "ong" if user["cnpj"] else "user" if user["cpf"] else ""
    token = jwt_bearer.sign_jwt(user["id"], role)
    return {"access_token": token}

@router.post("/refresh-token", dependencies=[Depends(jwt_bearer)])
async def refresh():
    token = jwt_bearer.refresh_jwt()
    return {"access_token": token}

@router.get("/profile", dependencies=[Depends(jwt_bearer)])
async def profile():
    id = jwt_bearer.get_user_id()
    roles = jwt_bearer.get_user_roles()
    response = login_service.get_user(id, roles)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.post("/register_ong")
async def register_ong(ong: OngModel = Body(..., example=OngModel.Config.json_schema_extra)):
    return RedirectResponse(url='/ong', status_code=http.HTTPStatus.TEMPORARY_REDIRECT)

@router.post("/register_adopter")
async def register_adopter(adopter: AdopterModel = Body(..., example=AdopterModel.Config.json_schema_extra)):
    return RedirectResponse(url='/adopter', status_code=http.HTTPStatus.TEMPORARY_REDIRECT)