import http
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import JSONResponse
from app.domain.models.animal import AnimalModel
from app.domain.models.dto.response import ResponseDTO
from app.services.animal_service import AnimalService
from app.services.ong_service import OngService
from app.services.jwt_service import JWTBearer

router = APIRouter(
    prefix="/ong/animals",
    tags=['animals_data']
)

ong_service = OngService()
animal_service = AnimalService(ong_service)
jwt_bearer = JWTBearer()

@router.get("/{animal_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_animal(request: Request, animal_id: str):
    request_id = request.state.request_id
    if ObjectId.is_valid(animal_id) is False:
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, "Invalid animal id", http.HTTPStatus.BAD_REQUEST).dict()
        )
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.get_animal(animal_id, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.post("/",dependencies=[Depends(jwt_bearer)], status_code=201)
async def create_animal(
    request: Request, 
    animal: AnimalModel = Body(..., example=AnimalModel.Config.json_schema_extra)
):
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.create_animal(animal, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )


@router.patch("/{animal_id}",dependencies=[Depends(jwt_bearer)], status_code=200)
async def update_animal(
    request: Request, 
    animal_id: str,
    animal: AnimalModel = Body(..., example=AnimalModel.Config.json_schema_extra)
):
    request_id = request.state.request_id
    if ObjectId.is_valid(animal_id) is False:
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, "Invalid animal id", http.HTTPStatus.BAD_REQUEST).dict()
        )
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.update_animal(animal, animal_id, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )