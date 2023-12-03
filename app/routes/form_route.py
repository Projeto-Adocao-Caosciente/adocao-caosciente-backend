from app.services.ong_service import OngService
from app.services.animal_service import AnimalService
from fastapi import APIRouter, Body, Depends, Request
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
async def create_form(
    request: Request,
    animal_id,
    form: FormModel = Body(..., example=FormModel.Config.json_schema_extra)):
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = form_service.create_form(ong_id, animal_id, form, request_id)
    return JSONResponse(
        status_code = response.status,
        content=response.dict()
    )


@router.get("/{animal_id}/", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_forms_from_animal(
    request: Request,
    animal_id: str
    ):
    print("get animal")
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = form_service.get_forms_from_animal(animal_id,ong_id, request_id)
    return JSONResponse(
        status_code = response.status,
        content=response.dict()
    )
    
@router.get("/questions/{animal_id}/{form_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def get_questions(
    request: Request, 
    animal_id:str, 
    form_id: str):
    print("question")
    ong_id = jwt_bearer.get_user_id()
    response = form_service.get_questions(ong_id, animal_id, form_id)
    return JSONResponse(
        status_code = response.status,
        content=response.dict()
    )

@router.get("/answers/{form_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_answers_sheet(
    request: Request,
    form_id: str
    ):
    print("answer")
    request_id = request.state.request_id
    response = form_service.get_answer_sheets(form_id,request_id)
    return JSONResponse(
        status_code = response.status,
        content=response.dict()
    )

# TODO: ler Form via ID, verificando se a ong tem permissão
@router.get("/{animal_id}/{form_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_form_by_id(animal_id:str, form_id: str, request: Request):
    print("read form by id")
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = form_service.get_form_by_id(ong_id, animal_id, form_id)
    #response = form_service.get_answer_sheets(form_id,request_id)
    return JSONResponse(
        status_code = response.status,
        content=response.dict()
    )