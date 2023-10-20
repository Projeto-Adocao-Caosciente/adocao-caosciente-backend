from typing import List
from pydantic import BaseModel


class Ong(BaseModel):
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
    animals: List[str] = []
    is_valid: bool = True

class Animal(BaseModel):
    ong: str
    photo: str # TODO
    name: str
    type: str
    breed: str
    height: float
    weight: float
    deficiency: List[str]
    special_needs: List[str]
    adoption_requirements: str
    adopter: str
    is_valid: bool = True

class Adopter(BaseModel):
    cpf: str
    name: str
    phone: str
    state: str
    city: str
    address: str
    number: int
    cep: str
    birthdate: str
    gender: str
    email: str
    animal: List[str]
    is_valid: bool = True
