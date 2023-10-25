from fastapi import APIRouter, Header, Response
from fastapi.encoders import jsonable_encoder

from app.domain.models.ong import OngModel
from app.services.ong_service import OngService
from bson import ObjectId

router = APIRouter(
    prefix="/ong",
    tags=['ongs_data']
)

ong_service = OngService()

@router.get("/{ong_id}", status_code=200)
async def read_ong(
    ong_id: str,
    authorization: str = Header(None),
):
    ong = ong_service.get_ong(ong_id)
    return {"message": "Ong retrieved successfully.", "data": { "ong": ong }}


@router.post("/", status_code=201)
async def create_ong(
    ong: OngModel,
    authorization: str = Header(None),
):
    ong_id = ong_service.create_ong(ong)
    return {"message": "Ong created successfully.", "id": str(ong_id)}


@router.put("/{ong_id}", status_code=200)
async def update_ong(
    ong: OngModel,
    ong_id: str,
    authorization: str = Header(None),
):
    ong_service.update_ong(ong, ong_id)
    return {"message": "Ong updated successfully."}


@router.delete(path="/{ong_id}", status_code=200)
async def delete_ong(
    ong_id: str,
    authorization: str = Header(None),
):
    ong_service.delete_ong(ong_id)
    return {"message": "Ong deleted successfully."}
