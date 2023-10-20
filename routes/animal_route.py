from fastapi import APIRouter, Header
from typing import List

from domain.entities import Animal

router = APIRouter(
    prefix="/animal",
    tags=['animals_data']
)

@router.post(
    path="/{animal_id}/{ong_cnpj}/{name}/{type}/{breed}/{height}/{weight}/{deficiency}/{special_needs}/{adoption_requirements}/{adopter_cpf}"
)
async def create_animal(
    animal_id: str,
    ong_cnpj: str,
    name: str,
    type: str,
    breed: str,
    height: float,
    weight: float,
    deficiency: List[str],
    special_needs: List[str],
    adoption_requirements: str,
    adopter: str,
    authorization: str = Header(None),
    status_code=200
):
    ong = Animal(
        id=animal_id,
        ong=ong_cnpj,
        name=name,
        type=type,
        breed=breed,
        height=height,
        weight=weight,
        deficiency=deficiency,
        special_needs=special_needs,
        adoption_requirements=adoption_requirements,
        adopter=adopter,
        is_valid=True
    ) # TODO


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
