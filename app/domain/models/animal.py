from pydantic import BaseModel

class AnimalModel(BaseModel):
    ong: str
    name: str
    type: str
    breed: str
    height: float
    weight: float
    deficiency: str
    special_needs: str
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
            'deficiency': self.deficiency,
            'special_needs': self.special_needs,
            'adoption_requirements': self.adoption_requirements,
            'photo': self.photo,
            'adopter': self.adopter,
        }