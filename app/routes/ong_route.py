from fastapi import APIRouter, Body, Depends
from app.domain.models.ong import OngModel
from app.services.jwt_service import JWTBearer
from app.services.ong_service import OngService

router = APIRouter(
    prefix="/ong",
    tags=['ongs_data']
)

ong_service = OngService()
jwt_bearer = JWTBearer()

@router.get("/", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_ong():
    ong_email = jwt_bearer.get_ong_user_id()
    ong = ong_service.get_ong(ong_email)
    return {"message": "Ong retrieved successfully.", "data": { "ong": ong }}

@router.get("/animals", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_ong_animals():
    ong_email = jwt_bearer.get_ong_user_id()
    animals = ong_service.get_ong_animals(ong_email)
    if len(animals) == 0:
        return {"message": "Ong has no animals.", "data": { "animals": animals }}
    return {"message": "Ong animals retrieved successfully.", "data": { "animals": animals }}

@router.post("/", status_code=201)
async def create_ong(ong: OngModel = Body(..., example=OngModel.Config.schema_extra)):
    result = ong_service.create_ong(ong)
    if result is None:
        return {"message": "Ong already exists."}
    return {"message": "Ong created successfully."}


@router.put("/", dependencies=[Depends(jwt_bearer)],  status_code=200)
async def update_ong(ong: OngModel = Body(..., example=OngModel.Config.schema_extra)):
    ong_email = jwt_bearer.get_ong_user_id()
    ong_service.update_ong(ong, ong_email)
    return {"message": "Ong updated successfully."}


# @router.delete(path="/", dependencies=[Depends(jwt_bearer)],  status_code=200)
# async def delete_ong():
#     ong_email = jwt_bearer.get_ong_user_id()
#     ong_service.delete_ong(ong_email)
#     return {"message": "Ong deleted successfully."}
