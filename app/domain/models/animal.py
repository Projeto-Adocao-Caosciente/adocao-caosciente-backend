from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class AnimalModel(BaseModel):
    name: str = Field(None, min_length=2, max_length=60)
    type: str = Field(None, min_length=2, max_length=60)
    breed: str = Field(None, min_length=2, max_length=60)
    height: str = Field(None, )
    weight: str = Field(None, )
    special_needs: Optional[List[str]] = [""]
    aditional_info: Optional[str] = Field(None, max_length=500) 
    adoption_requirements: List[str] = [""]
    photo: str = ""
    adopter: str = ""
    created_at: str = ""
    forms: list = []
    updated_at: str = datetime.now().isoformat()


    class Config:
        json_schema_extra = {
            "name": "Simba",
            "type": "Cat",
            "breed": "Orange",
            "height": "25cm",
            "weight": "2.830kg",
            "special_needs": ["Precisa de uma casa com quintal"],
            "aditional_info": "Necessita de carinho constante",
            "adoption_requirements": [],
            "photo": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMWFhUXGBgYGBgYGBgYGBgYGBgYGBgYGBgYHSggGBolHRgXITEhJSkrLi4uGB8zODMsNygtLisBCgo,",
            "adopter": "5f9d0a9f9d1a1d2d3d4d5d6"
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
            "adoption_requirements": animal["adoption_requirements"],
            "photo": animal["photo"],
            "adopter": animal["adopter"],
            "forms": [str(form) for form in animal["forms"]]
        }