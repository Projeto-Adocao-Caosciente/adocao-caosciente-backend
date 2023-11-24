from fastapi import APIRouter, Body, Depends
from app.domain.models.adopter import AdopterModel
from app.services.adopter_service import AdopterService
from app.services.jwt_service import JWTBearer

router = APIRouter(
    prefix="/adopter",
    tags=['adopte_data']
)

adopter_service = AdopterService()
jwt_bearer = JWTBearer()

@router.get("/", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_adopter():
    adopter_id = jwt_bearer.get_adopter_user_id()
    adopter = adopter_service.get_adopter_by_id(adopter_id)
    return {"message": "Adopter retrieved seccessully.", "data": {"addopter": adopter}}

@router.get("/animals", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_adopter_animals():
    adopter_id = jwt_bearer.get_adopter_user_id()
    animals = adopter_service.get_adopter_animals(adopter_id)
    if len(animals) == 0:
        return {"message": "Adopter has no animals.", "data": { "animals": animals }}
    return {"message": "Adopter animals retrieved successfully.", "data": { "animals": animals }}

@router.post("/", status_code=201)
async def create_adopter(adopter: AdopterModel = Body(..., example=AdopterModel.Config.schema_extra)):
    result = adopter_service.create_adopter(adopter)
    if result:
        return {"message": "Adopte created successfully."}
    return {"message": "Failed to create adopter."}
