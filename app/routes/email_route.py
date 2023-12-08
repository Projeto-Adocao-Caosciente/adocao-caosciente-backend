from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, Request
from app.domain.models.email import EmailModel
from app.services.email_service import EmailService


router = APIRouter(
    prefix="/email",
    tags=['email_operation']
)

email_service = EmailService()

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
