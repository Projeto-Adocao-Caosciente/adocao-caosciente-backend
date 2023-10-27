from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class AnimalModel(BaseModel):
    ong: str = Field("")
    name: str = Field(...)
    type: str = Field(...)
    breed: str = Field(...)
    height: str = Field(...)
    weight: str = Field(...)
    special_needs: List[str] = Field(...)
    adoption_requirements: List[str] = Field([]) # TODO: Isso provavelmente é o formulario = Field(...)
    photo: str = Field(...) # TODO
    created_at: str = Field("")
    updated_at: str = Field(datetime.now())
    adopter: str = Field(...)

    class Config:
        schema_extra = {
            "name": "Simba",
            "type": "Cat",
            "breed": "Orange",
            "height": "25cm",
            "weight": "2.830kg",
            "special_needs": ["Necessita de carinho constante", "Precisa de uma casa com quintal"],
            "adoption_requirements": [],
            "photo": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMWFhUXGBgYGBgYGBgYGBgYGBgYGBgYGBgYHSggGBolHRgXITEhJSkrLi4uGB8zODMsNygtLisBCgo,",
            "adopter": "5f9d0a9f9d1a1d2d3d4d5d6"
        }

    def __dict__(self) -> dict:
        return {
            'ong': self.ong,
            'name': self.name,
            'type': self.type,
            'breed': self.breed,
            'height': self.height,
            'weight': self.weight,
            'special_needs': self.special_needs,
            'photo': self.photo,
            'adopter': self.adopter,
        }
    
    @staticmethod
    def animal_helper(animal) -> dict:
        return {
            "id": str(animal["_id"]),
            "ong": animal["ong"],
            "name": animal["name"],
            "type": animal["type"],
            "breed": animal["breed"],
            "height": animal["height"],
            "weight": animal["weight"],
            "special_needs": animal["special_needs"],
            "adoption_requirements": animal["adoption_requirements"],
            "photo": animal["photo"],
            "adopter": animal["adopter"],
        }