from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.domain.models.animal import AnimalModel
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
    ong_id = jwt_bearer.get_ong_user_id()
    animal = animal_service.get_animal(animal_id, ong_id)
    if animal is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Animal not found.", "data": { "animal": animal }}
        )
    return JSONResponse(
        status_code=200,
        content={"message": "Animal retrieved successfully.", "data": { "animal": animal }}
    )

@router.post("/",dependencies=[Depends(jwt_bearer)], status_code=201)
async def create_animal(
    animal: AnimalModel = Body(..., example=AnimalModel.Config.json_schema_extra)
):
    # TODO: Validar se a a ong é valida de fato
    ong_id = jwt_bearer.get_ong_user_id()
    result = animal_service.create_animal(animal, ong_id)
    if result:
        return JSONResponse(
            status_code=201,
            content={"message": "Animal created successfully."}
        )
    return JSONResponse(
        status_code=500,
        content={"message": "Error creating animal."}
    )


@router.put("/{animal_id}",dependencies=[Depends(jwt_bearer)], status_code=200)
async def update_animal(
    animal_id: str,
    animal: AnimalModel = Body(..., example=AnimalModel.Config.json_schema_extra)
):
    # TODO: Validar se a a ong é valida de fato
    ong_id = jwt_bearer.get_ong_user_id()
    animal.ong = ong_id
    result = animal_service.update_animal(animal, animal_id)
    if result:
        return JSONResponse(
            status_code=200,
            content={"message": "Animal updated successfully."}
        )
    return JSONResponse(
        status_code=500,
        content={"message": "Error updating animal."}
    )


# @router.delete(path="/{animal_id}",dependencies=[Depends(jwt_bearer)], status_code=200)
# async def delete_animal(
#     animal_id: str,
# ):
#     animal_service.delete_animal(animal_id)
#     return {"message": "Animal deleted successfully."}
