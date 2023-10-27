from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class OngModel(BaseModel):
    cnpj: str = Field(...)
    name: str = Field(..., max_length=80)
    logo: str = Field(...)
    city: str = Field(..., max_length=50)
    state: str = Field(...)
    phone: str = Field(...)
    email: str = Field(..., validate_email=True) 
    mission: str = Field(..., max_length=150)
    foundation: str = Field(...,validate_regex=r"^\d{4}-\d{2}-\d{2}$") # YYYY-MM-DD
    description: str = Field(..., max_length=300)
    animals: List[str] = Field([])
    created_at: str = Field("")
    updated_at: str = Field(datetime.now())
    password: str  = Field(...)

    class Config:
        schema_extra = {
            "cnpj": "12345678901234",
            "name": "Ong Name",
            "logo": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMWFhUXGBgYGBgYGBgYGBgYGBgYGBgYGBgYHSggGBolHRgXITEhJSkrLi4uGB8zODMsNygtLisBCgo,",
            "city": "City Name",
            "state": "ST",
            "phone": "(11) 91234-5678",
            "email": "ong@email.com",
            "mission": "Ong mission",
            "foundation": "2023-10-27",
            "description": "Ong description",
            "password": "ong_password"
        }

    def __dict__(self) -> dict:
        return {
            'cnpj': self.cnpj,
            'name': self.name,
            'logo': self.logo,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'email': self.email,
            'mission': self.mission,
            'foundation': self.foundation,
            'animals': self.animals,
            'description': self.description,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': datetime.now(),
        }

    @staticmethod
    def ong_helper(ong) -> dict:
        return {
            "id": str(ong["_id"]),
            "cnpj": ong["cnpj"],
            "name": ong["name"],
            "logo": ong["logo"],
            "city": ong["city"],
            "state": ong["state"],
            "phone": ong["phone"],
            "email": ong["email"],
            "mission": ong["mission"],
            "foundation": ong["foundation"],
            "description": ong["description"],
            "created_at": ong["created_at"],
            "updated_at": ong["updated_at"],
        }