from pydantic import BaseModel
from typing import List

class AnimalModel(BaseModel):
    ong: str
    name: str
    type: str
    breed: str
    height: float
    weight: float
    special_needs: List[str]
    adoption_requirements: str
    photo: str # TODO 
    adopter: str

    def __dict__(self) -> dict:
        return {
            'ong': self.ong,
            'name': self.name,
            'type': self.type,
            'breed': self.breed,
            'height': self.height,
            'weight': self.weight,
            'special_needs': self.special_needs,
            'adoption_requirements': self.adoption_requirements,
            'photo': self.photo,
            'adopter': self.adopter,
        }