from fastapi import APIRouter, Header, Response
from fastapi.encoders import jsonable_encoder

from app.domain.models.animal import AnimalModel
from app.services.animal_service import AnimalService

router = APIRouter(
    prefix="/animal",
    tags=['animals_data']
)

animal_service = AnimalService()

@router.get("/{animal_id}", status_code=200)
async def read_animal(
    animal_id: str,
    authorization: str = Header(None),
):
    animal = animal_service.get_animal(animal_id)
    return {"message": "Animal retrieved successfully.", "data": { "animal": animal }}


@router.post("/")
async def create_animal(
    animal: AnimalModel,
    authorization: str = Header(None),
    status_code=200
):
    animal_id = animal_service.create_animal(animal)
    return  {"message": "Animal created successfully.", "id": str(animal_id)}


@router.put("/{animal_id}", status_code=200)
async def update_animal(
    animal: AnimalModel,
    animal_id: str,
    authorization: str = Header(None),
):
    animal_service.update_animal(animal, animal_id)
    return {"message": "Animal updated successfully."}


@router.delete(path="/{animal_id}", status_code=200)
async def delete_animal(
    animal_id: str,
    authorization: str = Header(None),
):
    animal_service.delete_animal(animal_id)
    return {"message": "Animal deleted successfully."}
