from fastapi import APIRouter, Depends, Header
from app.domain.models.animal import AnimalModel
from app.services.animal_service import AnimalService
from app.services.ong_service import OngService
from app.services.jwt_service import JWTBearer

router = APIRouter(
    prefix="/animal",
    tags=['animals_data']
)

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
    animal: AnimalModel,
):
    animal_id = animal_service.create_animal(animal)
    return  {"message": "Animal created successfully.", "id": str(animal_id)}


@router.put("/{animal_id}",dependencies=[Depends(jwt_bearer)], status_code=200)
async def update_animal(
    animal: AnimalModel,
    animal_id: str,
):
    animal_service.update_animal(animal, animal_id)
    return {"message": "Animal updated successfully."}


@router.delete(path="/{animal_id}",dependencies=[Depends(jwt_bearer)], status_code=200)
async def delete_animal(
    animal_id: str,
):
    animal_service.delete_animal(animal_id)
    return {"message": "Animal deleted successfully."}
