from typing import List
from pydantic import BaseModel, Field


class EmailModel(BaseModel):
    form_id: str = Field(None, )
    recipient_emails: List[str] = Field(None, max_length=60)

    class Config:
        json_schema_extra = {
            "form_id": "60c7d9e4d9b9e2e4c3c3e2e4",
            "recipient_emails": ["email1@gmail.com", "email2@gmail.com"],
        }
