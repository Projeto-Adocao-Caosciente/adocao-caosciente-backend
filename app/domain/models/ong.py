from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel, Field
from app.utils.mask import Mask
from app.utils.utils import Utils

class OngModel(BaseModel):
    cnpj: str = None
    name: str = None
    logo: str = None
    city: str = None
    state: str = None
    phone: str = None
    email: str = None
    mission: str = None 
    foundation: str = None # YYYY-MM-DD
    description: str = None 
    animals: List[str] =  []   
    created_at: str = None
    updated_at: str = datetime.now().isoformat()
    password: str = None

    class Config:
        json_schema_extra = {
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
            'phone': Utils.convert_to_digit(self.phone),
            'email': self.email,
            'mission': self.mission,
            'foundation': self.foundation,
            'animals': self.animals,
            'description': self.description,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    @staticmethod
    def helper(ong) -> dict:
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
