from typing import List
from pydantic import BaseModel


class Ong_input(BaseModel):
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
    password: str

class Ong_database(BaseModel):
    id: str
    cnpj: str
    name: str
    # logo: str # TODO
    city: str
    state: str
    phone: str
    email: str
    mission: str
    foundation: str
    description: str
    password: str
    animals: List[str] = []
    is_deleted: bool = False


class Animal(BaseModel):
    id: str
    ong: str
    photo: str
    name: str
    type: str
    breed: str
    height: float
    weight: float
    special_needs: List[str]
    adoption_requirements: str # TODO
    adopter: str
    is_deleted: bool = False

class Adopter(BaseModel):
    id: str
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

class Login(BaseModel):
    user: str
    password: str
