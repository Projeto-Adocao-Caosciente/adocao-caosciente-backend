from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, Request
from app.domain.models.email import EmailModel
from app.services.animal_service import AnimalService
from app.services.form_service import FormService
from app.services.email_service import EmailService
from app.services.ong_service import OngService


router = APIRouter(
    prefix="/email",
    tags=['email_operation']
)

ong_service = OngService()
animal_service = AnimalService(ong_service)
form_service = FormService(ong_service, animal_service)
email_service = EmailService(form_service)

@router.post("/send", status_code=201)
async def send_email(
    request: Request,
    email: EmailModel = Body(..., example=EmailModel.Config.json_schema_extra)
):
    request_id = request.state.request_id

    response = email_service.send_email(email, request_id)

    return JSONResponse(
        status_code=response.status,
        content=response.dict()
    )
