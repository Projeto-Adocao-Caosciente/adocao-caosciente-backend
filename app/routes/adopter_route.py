from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.domain.models.adopter import AdopterModel
from app.services.adopter_service import AdopterService
from app.services.jwt_service import JWTBearer

router = APIRouter(
    prefix="/adopter",
    tags=['adopter_data']
)

adopter_service = AdopterService()
jwt_bearer = JWTBearer()

@router.post("/", status_code=201)
async def create_adopter(adopter: AdopterModel = Body(..., example=AdopterModel.Config.json_schema_extra)):
    adopter.remove_mask_cpf()
    adopter.remove_mask_cep()
    adopter.remove_mask_phone()
    
    response = adopter_service.create_adopter(adopter)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_adopter():
    adopter_id = jwt_bearer.get_user_id()
    response = adopter_service.get_adopter_by_id(adopter_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/animals", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_adopter_animals():
    adopter_id = jwt_bearer.get_adopter_user_id()
    response = adopter_service.get_adopter_animals(adopter_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

