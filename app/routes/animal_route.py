from fastapi import APIRouter, Body, Depends
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
    ong_email = jwt_bearer.get_ong_user_id()
    animal = animal_service.get_animal(animal_id, ong_email)
    if animal is None:
        return {"message": "Animal not found.", "data": { "animal": animal }}
    return {"message": "Animal retrieved successfully.", "data": { "animal": animal }}

@router.post("/",dependencies=[Depends(jwt_bearer)], status_code=201)
async def create_animal(
    animal: AnimalModel = Body(..., example=AnimalModel.Config.schema_extra)
):
    # TODO: Validar se a a ong é valida de fato
    ong_email = jwt_bearer.get_ong_user_id()
    ong = OngService().get_ong_by_email(ong_email)
    if ong is None:
        return {"message": "Error creating animal. Ong not found."}
    animal.ong = ong["cnpj"]
    result = animal_service.create_animal(animal)
    if result:
        return  {"message": "Animal created successfully."}
    return {"message": "Error creating animal."}


@router.put("/{animal_id}",dependencies=[Depends(jwt_bearer)], status_code=200)
async def update_animal(
    animal_id: str,
    animal: AnimalModel = Body(..., example=AnimalModel.Config.schema_extra)
):
    # TODO: Validar se a a ong é valida de fato
    ong_email = jwt_bearer.get_ong_user_id()
    animal.ong = ong_email
    result = animal_service.update_animal(animal, animal_id)
    if result:
        return  {"message": "Animal updated successfully."}
    return {"message": "Error updating animal."}


# @router.delete(path="/{animal_id}",dependencies=[Depends(jwt_bearer)], status_code=200)
# async def delete_animal(
#     animal_id: str,
# ):
#     animal_service.delete_animal(animal_id)
#     return {"message": "Animal deleted successfully."}
