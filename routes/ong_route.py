from fastapi import APIRouter, Header

from domain.entities import Ong

router = APIRouter(
    prefix="/ong",
    tags=['ongs_data']
)

@router.post(
    path="/{ong_id}/{cnpj}/{name}/{city}/{state}/{phone}/{email}/{mission}/{foundation}/{description}"
)
async def create_ong(
    ong_id: str,
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
        id=ong_id,
        cnpj=cnpj,
        name=name,
        city=city,
        state=state,
        phone=phone,
        email=email,
        mission=mission,
        foundation=foundation,
        description=description,
        animals=[],
        is_valid=True
    ) # TODO


@router.get(
    path="/{ong_id}"
)
async def read_ong(
    ong_id: str,
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
    path="/{ong_id}"
)
async def delete_ong(
    ong_id: str,
    authorization: str = Header(None),
    status_code=200
):
    pass # TODO
