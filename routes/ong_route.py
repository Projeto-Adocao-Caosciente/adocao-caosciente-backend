from fastapi import APIRouter, Header

from domain.entities import Ong_input, Login

router = APIRouter(
    prefix="/ong",
    tags=['ongs_data']
)

@router.post("/")
async def create_ong(
    ong: Ong_input,
    authorization: str = Header(None),
    status_code=200
):
    print(ong)
    return {"Hello": "World"}


@router.put("/")
async def update_ong(
    ong: Ong_input,
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
