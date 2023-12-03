from app.services.ong_service import OngService
from app.services.animal_service import AnimalService
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import JSONResponse
from app.domain.models.form import FormModel
from app.services.jwt_service import JWTBearer
from app.services.form_service import FormService
import http

router = APIRouter(
    prefix="/forms",
    tags=['form_data']
)

ong_service = OngService()
animal_service = AnimalService(ong_service)
form_service = FormService(ong_service, animal_service)
jwt_bearer = JWTBearer()

# This route can be used to get a questions list from adopter form
@router.get("/questions/{form_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def get_questions(
        request: Request,
        form_id: str
):
    request_id = request.state.request_id
    response = form_service.get_questions(form_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/answers/{form_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_answers_sheet(
    request: Request,
    form_id: str
):
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = form_service.get_answer_sheets(form_id, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.get("/{animal_id}", dependencies=[Depends(jwt_bearer)])
def get_forms_from_animal(
    request: Request,
    animal_id: str
):
    """
    Retrieve forms belonging to the animal.
    """
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = animal_service.get_forms_from_animal(animal_id, ong_id, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

@router.post("/{animal_id}", dependencies=[Depends(jwt_bearer)], status_code=201)
async def create_form(request: Request, animal_id, form: FormModel = Body(..., example=FormModel.Config.json_schema_extra)):
    required_fields = form.required_field_at_create()
    receveid_fields = set(
        [key for key, value in form.model_dump().items() if value is not None])
    if not required_fields.issubset(receveid_fields):
        return JSONResponse(
            status_code=http.HTTPStatus.BAD_REQUEST,
            content={"message": f"Required fields: {required_fields}"}
        )

    ong_id = jwt_bearer.get_user_id()

    request_id = request.state.request_id

    response = form_service.create_form(ong_id, animal_id, form, request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )

# TODO: ler Form via ID, verificando se a ong tem permissão


@router.get("/{animal_id}/{form_id}", dependencies=[Depends(jwt_bearer)], status_code=200)
async def read_form_by_id(animal_id: str, form_id: str, request: Request):
    request_id = request.state.request_id
    ong_id = jwt_bearer.get_user_id()
    response = form_service.get_form_by_id(ong_id, animal_id, form_id)
    # response = form_service.get_answer_sheets(form_id,request_id)
    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )
