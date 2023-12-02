import http
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import JSONResponse
from app.domain.models.adopter import AdopterModel
from app.domain.models.animal import AnimalModel
from app.domain.models.dto.response import ResponseDTO
from app.services.adopter_service import AdopterService
from app.services.jwt_service import JWTBearer

router = APIRouter(
    prefix="/adopter",
    tags=['adopter_data']
)

adopter_service = AdopterService()
jwt_bearer = JWTBearer()

@router.post("/", status_code=201)
async def create_adopter(request: Request, adopter: AdopterModel = Body(..., example=AdopterModel.Config.json_schema_extra)):
    required_fields = adopter.required_field_at_create()
    received_fields = set([ key for key, value in adopter.model_dump().items() if value is not None ])
    if not required_fields.issubset(received_fields):
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content=ResponseDTO(None, f"Missing required fields: {required_fields - received_fields}", http.HTTPStatus.BAD_REQUEST).dict()
        )

    adopter.remove_mask_cpf()
    adopter.remove_mask_cep()
    adopter.remove_mask_phone()

    request_id = request.state.request_id
    
    response = adopter_service.create_adopter(adopter, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/", dependencies=[Depends(jwt_bearer)])
async def read_adopter(request: Request):
    request_id = request.state.request_id
    adopter_id = jwt_bearer.get_user_id()
    response = adopter_service.get_adopter_by_id(adopter_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.patch("/", dependencies=[Depends(jwt_bearer)])
async def update_ong(
    request: Request,
    adopter: AdopterModel = Body(..., example=AdopterModel.Config.json_schema_extra)
):
    adopter.remove_mask_cpf()
    adopter.remove_mask_cep()
    adopter.remove_mask_phone()

    request_id = request.state.request_id

    adopter_id = jwt_bearer.get_user_id()
    response = adopter_service.update_adopter(adopter, adopter_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/animals", dependencies=[Depends(jwt_bearer)])
async def read_adopter_animals(request: Request):
    request_id = request.state.request_id
    adopter_id = jwt_bearer.get_user_id()
    response = adopter_service.get_adopter_animals(adopter_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/animals/{animal_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_animal(request: Request, animal_id: str):
    """
    Retrieve an animal belonging to the adopter.
    """
    return JSONResponse(
        status_code=http.HTTPStatus.NOT_IMPLEMENTED,
        content=ResponseDTO(None, "In construction", http.HTTPStatus.NOT_IMPLEMENTED).dict()
    )
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

@router.post("/request-adoption/{animal_id}", dependencies=[Depends(jwt_bearer)], status_code=201)
async def request_adoption(
    request: Request, 
    animal_id: str,
):
    """
    Request adoption of an existing Animal belonging to the ong.
    """
    return JSONResponse(
        status_code=http.HTTPStatus.NOT_IMPLEMENTED,
        content=ResponseDTO(None, "In construction", http.HTTPStatus.NOT_IMPLEMENTED).dict()
    )
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.create_animal(animal, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )