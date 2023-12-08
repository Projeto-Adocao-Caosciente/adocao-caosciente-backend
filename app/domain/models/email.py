from pydantic import BaseModel, Field

from app.config.settings import settings


class EmailModel(BaseModel):
    adopter_name: str = Field(None, max_length=60)
    animal_name: str = Field(None, max_length=60)
    form_link: str = Field(None, )
    sender_email: str = "adocaocaosciente@gmail.com"
    recipient_email: str = Field(None, max_length=60)
    subject: str = "Adocãosciente: formulário de adoção"
    password: str = settings.EMAIL_PASSWORD

    class Config:
        json_schema_extra = {
            "adopter_name": "Adopter name",
            "animal_name": "Animal name",
            "form_link": "formlink.com",
            "recipient_email": "recipient_email@gmail.com",
        }
