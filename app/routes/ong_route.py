from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
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
    ong_id = jwt_bearer.get_ong_user_id()
    ong = ong_service.get_ong_by_id(ong_id)
    return JSONResponse(
        status_code=200,
        content={"message": "Ong retrieved successfully.", "data": { "ong": ong }}
    )

@router.get("/animals", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_ong_animals():
    ong_id = jwt_bearer.get_ong_user_id()
    animals = ong_service.get_ong_animals(ong_id)
    if len(animals) == 0:
        return JSONResponse(
            status_code=404,
            content={"message": "Ong has no animals.", "data": { "animals": animals }}
        )
    return JSONResponse(
        status_code=200,
        content={"message": "Ong animals retrieved successfully.", "data": { "animals": animals }}
    )

@router.post("/", status_code=201)
async def create_ong(ong: OngModel = Body(..., example=OngModel.Config.json_schema_extra)):
    response = ong_service.create_ong(ong)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )


@router.patch("/", dependencies=[Depends(jwt_bearer)])
async def update_ong(ong: OngModel = Body(..., example=OngModel.Config.json_schema_extra)):
    ong_id = jwt_bearer.get_ong_user_id()
    response = ong_service.update_ong(ong, ong_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )


@router.delete(path="/", dependencies=[Depends(jwt_bearer)],  status_code=200)
async def delete_ong():
    ong_id = jwt_bearer.get_ong_user_id()
    result = ong_service.delete_ong(ong_id)
    if result:
        return JSONResponse(
            status_code=200,
            content={"message": "Ong deleted successfully."}
        )
    return JSONResponse(
        status_code=500,
        content={"message": "Error deleting Ong"}
    )
