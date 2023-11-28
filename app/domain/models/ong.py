from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class OngModel(BaseModel):
    cnpj: str = Field(None, min_length=14, max_length=14)
    name: str = Field(None, min_length=2, max_length=60)
    logo: str = Field(None, )
    city: str = Field(None, min_length=2, max_length=60)
    state: str = Field(None, min_length=2, max_length=60)
    phone: str = Field(None, min_length=10, max_length=12)
    email: str = Field(None, max_length=60)
    mission: str = Field(None, max_length=500)
    foundation: str = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    description: Optional[str] = Field(None, max_length=500) 
    animals: List[str] = Field([], )
    created_at: str = Field(None, )
    updated_at: str = datetime.now().isoformat()
    password: str = Field(None, min_length=4, max_length=60)
    
    def required_field_at_create(self) -> set:
        return {"cnpj", "name", "logo", "city", "state", "phone", "email", "mission", "foundation", "description", "password"}

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
            'phone': self.phone,
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
        
    def remove_mask_cnpj(self):
        cnpj_normalized = self.model_dump()["cnpj"].replace(".", "").replace("/", "").replace("-", "")
        self.cnpj = cnpj_normalized
        
    def remove_mask_phone(self):
        phone_normalized = self.model_dump()["phone"].replace("(", "").replace(")", "").replace(" ", "").replace(".", "").replace("/", "").replace("-", "")
        self.phone = phone_normalized