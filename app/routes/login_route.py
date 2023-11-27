from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.domain.models.login import LoginModel
from app.domain.models.ong import OngModel
from app.domain.models.adopter import AdopterModel
from app.services.login_service import LoginService
from app.services.jwt_service import JWTBearer

router = APIRouter(
    prefix="",
    tags=['authentication']
)

login_service = LoginService()

@router.post("/login", status_code=200)
async def login(
    login: LoginModel,
):
    user = login_service.authenticate(login.user, login.password)
    token = JWTBearer.sign_jwt(user["id"])
    return {"access_token": token, "user": user}

@router.post("/register_ong", status_code=201)
async def register_ong(ong: OngModel):
    response = login_service.register(ong)
    return JSONResponse(
        status_code=response.status,
        content=response.model_dump()
    )

@router.post("/register_adopter", status_code=201)
async def register_adopter(adopter: AdopterModel):
    response = login_service.register(adopter)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

    
@router.post("/refresh", status_code=200)
async def refresh():
    # TODO: implementar refresh
    return {"message": "Refresh successfully."}