from fastapi import APIRouter, Header

from domain.entities import Ong

router = APIRouter(
    prefix="/ong",
    tags=['ongs_data']
)

@router.post(
    path="/{cnpj}/{name}/{city}/{state}/{phone}/{email}/{mission}/{foundation}/{description}"
)
async def create_ong(
    cnpj: str,
    name: str,
    city: str,
    state: str,
    phone: str,
    email: str,
    mission: str,
    foundation: str,
    description: str,
    authorization: str = Header(None),
    status_code=200
):
    ong = Ong(
        cnpj=cnpj,
        name=name,
        city=city,
        state=state,
        phone=phone,
        email=email,
        mission=mission,
        foundation=foundation,
        description=description,
    ) # TODO


@router.get(
    path="/{cnpj}"
)
async def read_ong(
    cnpj: str,
    authorization: str = Header(None),
    status_code=200
):
    pass # TODO


@router.put("/")
async def update_ong(
    ong: Ong,
    authorization: str = Header(None),
    status_code=200
):
    pass # TODO


@router.delete(
    path="/{cnpj}"
)
async def delete_ong(
    cnpj: str,
    authorization: str = Header(None),
    status_code=200
):
    pass # TODO
