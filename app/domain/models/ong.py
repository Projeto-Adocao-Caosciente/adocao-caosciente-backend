from typing import List
from pydantic import BaseModel

class OngModel(BaseModel):
    cnpj: str
    name: str
    logo: str # TODO
    city: str
    state: str
    phone: str
    email: str
    mission: str
    foundation: str
    description: str
    animals: List[str]
    password: str

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
            'description': self.description,
            'password': self.password,
        }

