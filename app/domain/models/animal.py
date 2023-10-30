from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class AnimalModel(BaseModel):
    name: str = ""
    type: str = ""
    breed: str = ""
    height: str = ""
    weight: str = ""
    special_needs: Optional[List[str]] = [""]
    aditional_info: Optional[str] = ""
    adoption_requirements: List[str] = [""]
    photo: str = ""
    adopter: str = ""
    created_at: str = ""
    updated_at: str = datetime.now()

    class Config:
        schema_extra = {
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
    def animal_helper(animal) -> dict:
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
        }