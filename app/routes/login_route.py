from fastapi import APIRouter
from app.domain.models.login import LoginModel
from app.domain.models.ong import OngModel
from app.services.login_service import LoginService
from app.services.jwt_service import JWTBearer
from app.services.ong_service import OngService

router = APIRouter(
    prefix="",
    tags=['authentication']
)

login_service = LoginService()

@router.post("/login", status_code=200)
async def login(
    login: LoginModel,
):
    ong = login_service.authenticate(login.user, login.password)
    token = JWTBearer.sign_jwt(ong["email"])
    return {"access_token": token, "user": ong}

@router.post("/register", status_code=201)
async def register(ong: OngModel):
    return login_service.register(ong)
    
@router.post("/refresh", status_code=200)
async def refresh():
    # TODO: implementar refresh
    return {"message": "Refresh successfully."}