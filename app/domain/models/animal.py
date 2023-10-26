from typing import List
from pydantic import BaseModel

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