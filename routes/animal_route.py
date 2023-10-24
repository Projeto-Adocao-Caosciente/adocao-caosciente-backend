from fastapi import APIRouter, Header
from typing import List

from domain.entities import Animal

router = APIRouter(
    prefix="/animal",
    tags=['animals_data']
)

@router.post("/")
async def create_animal(
    animal: Animal,
    authorization: str = Header(None),
    status_code=200
):
    pass


@router.get(
    path="/{animal_id}"
)
async def read_animal(
    animal_id: str,
    authorization: str = Header(None),
    status_code=200
):
    pass # TODO


@router.put("/")
async def update_animal(
    animal: Animal,
    authorization: str = Header(None),
    status_code=200
):
    pass # TODO


@router.delete(
    path="/{animal_id}"
)
async def delete_animal(
    animal_id: str,
    authorization: str = Header(None),
    status_code=200
):
    pass # TODO
