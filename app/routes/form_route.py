from app.services.ong_service import OngService
from app.services.animal_service import AnimalService
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from app.domain.models.form import FormModel
from app.services.jwt_service import JWTBearer
from app.services.form_service import FormService

router = APIRouter(
    prefix="/form",
    tags=['form_data']
)

ong_service = OngService()
animal_service = AnimalService(ong_service)
form_service = FormService(ong_service, animal_service)
jwt_bearer = JWTBearer()

@router.post("/{animal_id}", dependencies=[Depends(jwt_bearer)], status_code=201)
async def create_form(animal_id, form: FormModel = Body(..., example=FormModel.Config.json_schema_extra)):
    ong_id = jwt_bearer.get_ong_user_id()
    response = form_service.create_form(ong_id, animal_id, form)
    return JSONResponse(
        status_code = response.status,
        content=response.dict()
    )

# TODO: ler Form via ID, verificando se a ong tem permissão
@router.get("/{animal_id}/{form_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def get_form(animal_id:str, form_id: str):
    ong_id = jwt_bearer.get_ong_user_id()
    response = form_service.get_form_by_id(ong_id, animal_id, form_id)
    return JSONResponse(
        status_code = response.status,
        content=response.dict()
    )
    
@router.get("/questions/{animal_id}/{form_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def get_questions(animal_id:str, form_id: str):
    ong_id = jwt_bearer.get_ong_user_id()
    response = form_service.get_questions(ong_id, animal_id, form_id)
    return JSONResponse(
        status_code = response.status,
        content=response.dict()
    )
    




