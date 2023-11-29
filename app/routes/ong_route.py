import logging
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import JSONResponse
from app.domain.models.ong import OngModel
from app.services.jwt_service import JWTBearer
from app.services.ong_service import OngService
from fastapi.responses import JSONResponse
import http
from app.domain.models.dto.response import ResponseDTO

router = APIRouter(
    prefix="/ong",
    tags=['ongs_data']
)

ong_service = OngService()
jwt_bearer = JWTBearer()

logger = logging.getLogger(__name__)

@router.get("/", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_ong(request: Request):
    request_id = request.state.requestId
    ong_id = jwt_bearer.get_user_id()
    response = ong_service.get_ong_by_id(ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/animals", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_ong_animals():
    ong_id = jwt_bearer.get_user_id()
    response = ong_service.get_ong_animals(ong_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.post("/", status_code=201)
async def create_ong(
    ong: OngModel = Body(..., example=OngModel.Config.json_schema_extra)
):
    required_fields = ong.required_field_at_create()
    received_fields = set([ key for key, value in ong.model_dump().items() if value is not None ])
    if not required_fields.issubset(received_fields):
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, f"Missing required fields: {required_fields - received_fields}",http.HTTPStatus.BAD_REQUEST).dict()
        )

    ong.remove_mask_cnpj()
    ong.remove_mask_phone()
    
    response = ong_service.create_ong(ong)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )


@router.patch("/", dependencies=[Depends(jwt_bearer)])
async def update_ong(
    ong: OngModel = Body(..., example=OngModel.Config.json_schema_extra)
):
    ong.remove_mask_cnpj()
    ong.remove_mask_phone()
    
    ong_id = jwt_bearer.get_user_id()
    response = ong_service.update_ong(ong, ong_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )
    