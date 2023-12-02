from app.services.ong_service import OngService
from app.services.animal_service import AnimalService
from fastapi import APIRouter, Body, Depends, Request
from fastapi.responses import JSONResponse
from app.domain.models.answerSheet import AnswerSheetModel
from app.services.jwt_service import JWTBearer
from app.services.form_service import FormService
from app.services.answer_sheet_service import AnswerSheetService
from app.services.adopter_service import AdopterService
from app.domain.models.dto.response import ResponseDTO

router = APIRouter(
    prefix="/answer",
    tags=['answer_sheet']
)

# TODO: Formulário está altamente acoplado com outras classes
ong_service = OngService()
animal_service = AnimalService(ong_service)
form_service = FormService(ong_service, animal_service)
adopter_service = AdopterService()
answerService = AnswerSheetService(form_service, adopter_service)
jwt_bearer = JWTBearer()

@router.post("/{form_id}", dependencies=[Depends(jwt_bearer)], status_code=201)
async def answer_form(
    request: Request,
    form_id: str,
    answer_sheet: AnswerSheetModel = Body(..., example=AnswerSheetModel.Config.schema_extra)
):
    request_id = request.state.request_id
    adopter_id = jwt_bearer.get_user_id()
    response = answerService.create_answer_sheet(adopter_id, form_id, answer_sheet, request_id)
    return JSONResponse(
        status_code = response.status,
        content = response.dict()
    )