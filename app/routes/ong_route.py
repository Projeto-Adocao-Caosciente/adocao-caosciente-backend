import logging
from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.responses import JSONResponse
from app.domain.models.animal import AnimalModel
from app.domain.models.ong import OngModel
from app.services.animal_service import AnimalService
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
animal_service = AnimalService(ong_service)
jwt_bearer = JWTBearer()

logger = logging.getLogger(__name__)

@router.get("/", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_ong(
    request: Request,
):
    """
    Retrieve the details of the authenticated user's ong.

    This endpoint requires a valid JWT token in the Authorization header.

    """
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = ong_service.get_ong_by_id(ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )


@router.post("/", status_code=201)
async def create_ong(
    request: Request,
    ong: OngModel = Body(..., example=OngModel.Config.json_schema_extra)
):
    """
    Create a new Ong.

    This endpoint allows you to create a new Ong by providing the required fields in the request body.

    Args:
        request (Request): The incoming request.
        ong (OngModel): The Ong data to be created.

    """
    required_fields = ong.required_field_at_create()
    received_fields = set([ key for key, value in ong.model_dump().items() if value is not None ])
    if not required_fields.issubset(received_fields):
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, f"Missing required fields: {required_fields - received_fields}",http.HTTPStatus.BAD_REQUEST).dict()
        )

    request_id = request.state.request_id

    ong.remove_mask_cnpj()
    ong.remove_mask_phone()
    
    response = ong_service.create_ong(ong, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )


@router.patch("/", dependencies=[Depends(jwt_bearer)])
async def update_ong(
    request: Request,
    ong: OngModel = Body(..., example=OngModel.Config.json_schema_extra)
):
    """
    Update an existing Ong.

    This endpoint allows you to update the information of an existing Ong.
    
    Parameters:
    - request: The incoming request object.
    - ong: The updated Ong object. (Example: OngModel.Config.json_schema_extra)


    """
    ong.remove_mask_cnpj()
    ong.remove_mask_phone()

    request_id = request.state.request_id
    
    ong_id = jwt_bearer.get_user_id()
    response = ong_service.update_ong(ong, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/animals", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_ong_animals(
    request: Request,
    name: Optional[str] = Query(default=None, description="Filter animals by name")
):
    """
    Retrieve animals belonging to the ong.
    
    If the 'name' query parameter is provided, it will filter animals by name.
    """
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    if name is None:
        response = ong_service.get_ong_animals(ong_id, request_id)
    else:
        response = ong_service.get_ong_animals_by_name(name, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/animals/{animal_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_animal(request: Request, animal_id: str):
    """
    Retrieve an animal belonging to the ong.

    """
    request_id = request.state.request_id
    if ObjectId.is_valid(animal_id) is False:
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, "Invalid animal id", http.HTTPStatus.BAD_REQUEST).dict()
        )
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.get_animal(animal_id, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.post("/animals",dependencies=[Depends(jwt_bearer)], status_code=201)
async def create_animal(
    request: Request, 
    animal: AnimalModel = Body(..., example=AnimalModel.Config.json_schema_extra)
):
    """
    Create a new Animal belonging to the ong.
    """
    required_fields = animal.required_field_at_create()
    received_fields = set([ key for key, value in animal.model_dump().items() if value is not None ])
    if not required_fields.issubset(received_fields):
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, f"Missing required fields: {required_fields - received_fields}", http.HTTPStatus.BAD_REQUEST).dict()
        )
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.create_animal(animal, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )


@router.patch("/animals/{animal_id}",dependencies=[Depends(jwt_bearer)], status_code=200)
async def update_animal(
    request: Request, 
    animal_id: str,
    animal: AnimalModel = Body(..., example=AnimalModel.Config.json_schema_extra)
):
    """
    Update an existing Animal belonging to the ong.
    """
    request_id = request.state.request_id
    if ObjectId.is_valid(animal_id) is False:
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, "Invalid animal id", http.HTTPStatus.BAD_REQUEST).dict()
        )
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.update_animal(animal, animal_id, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )