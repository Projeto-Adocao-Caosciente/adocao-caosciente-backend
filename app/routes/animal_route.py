import http
from bson import ObjectId
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.domain.models.animal import AnimalModel
from app.domain.models.dto.response import ResponseDTO
from app.services.animal_service import AnimalService
from app.services.ong_service import OngService
from app.services.jwt_service import JWTBearer

router = APIRouter(
    prefix="/animal",
    tags=['animals_data']
)

# TODO: Fazer injeção de dependencia da forma correta (não sei como kkkk)

ong_service = OngService()
animal_service = AnimalService(ong_service)
jwt_bearer = JWTBearer()

@router.get("/{animal_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_animal(animal_id: str):
    if ObjectId.is_valid(animal_id) is False:
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, "Invalid animal id", http.HTTPStatus.BAD_REQUEST).dict()
        )
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.get_animal(animal_id, ong_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.post("/",dependencies=[Depends(jwt_bearer)], status_code=201)
async def create_animal(
    animal: AnimalModel = Body(..., example=AnimalModel.Config.json_schema_extra)
):
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.create_animal(animal, ong_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )


@router.patch("/{animal_id}",dependencies=[Depends(jwt_bearer)], status_code=200)
async def update_animal(
    animal_id: str,
    animal: AnimalModel = Body(..., example=AnimalModel.Config.json_schema_extra)
):
    if ObjectId.is_valid(animal_id) is False:
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, "Invalid animal id", http.HTTPStatus.BAD_REQUEST).dict()
        )
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.update_animal(animal, animal_id, ong_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )