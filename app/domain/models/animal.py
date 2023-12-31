from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class AnimalModel(BaseModel):
    name: str = Field(None, min_length=2, max_length=60)
    type: str = Field(None, min_length=2, max_length=60)
    breed: str = Field(None, min_length=2, max_length=60)
    height: str = Field(None, )
    weight: str = Field(None, )
    special_needs: Optional[List[str]] = None
    aditional_info: Optional[str] = Field(None, max_length=500) 
    photo: str = None
    adopter: str = None
    forms: list = []
    created_at: str = None
    updated_at: str = datetime.now().isoformat()

    def required_field_at_create(self) -> set:
        return {"name", "type", "breed", "height", "weight", "photo" }

    class Config:
        json_schema_extra = {
            "name": "Simba",
            "type": "Cat",
            "breed": "Orange",
            "height": "25cm",
            "weight": "2.830kg",
            "special_needs": ["Precisa de uma casa com quintal"],
            "aditional_info": "Necessita de carinho constante",
            "photo": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMWFhUXGBgYGBgYGBgYGBgYGBgYGBgYGBgYHSggGBolHRgXITEhJSkrLi4uGB8zODMsNygtLisBCgo,",
        }

    def __dict__(self) -> dict:
        return {
            'name': self.name,
            'type': self.type,
            'breed': self.breed,
            'height': self.height,
            'weight': self.weight,
            'special_needs': self.special_needs,
            'aditional_info': self.aditional_info,
            'adoption_requirements': self.adoption_requirements,
            'photo': self.photo,
            'adopter': self.adopter,
        }
    
    @staticmethod
    def helper(animal) -> dict:
        return {
            "id": str(animal["_id"]),
            "name": animal["name"],
            "type": animal["type"],
            "breed": animal["breed"],
            "height": animal["height"],
            "weight": animal["weight"],
            "special_needs": animal["special_needs"],
            "aditional_info": animal["aditional_info"],
            "photo": animal["photo"],
            "adopter": animal["adopter"],
            "created_at": animal["created_at"],
            "updated_at": animal["updated_at"]
        }