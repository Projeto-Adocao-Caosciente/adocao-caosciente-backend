from datetime import datetime
from typing import List
from pydantic import BaseModel


class AdopterModel(BaseModel):
    cpf: str = ""
    name: str = ""
    phone: str = ""
    state: str = ""
    city: str = ""
    address: str = ""
    number: str = ""
    cep: str = ""
    birthdate: str = ""
    gender: str = ""
    email: str = ""
    photo: str = ""
    animals: List[str] =  []
    responses: List[str] = []
    created_at: str = ""
    updated_at: str = datetime.now()
    password: str = ""

    class Config:
        schema_extra = {
            "cpf": "12345678901",
            "name": "I Ryan Maiden",
            "phone": "(11) 98765-4321",
            "state": "ST",
            "city": "City Name",
            "address": "Address Name",
            "number": "10",
            "cep": "12.345-678",
            "birthdate": "2003-01-01",
            "gender": "Masculine",
            "email": "adopter@gmail.com",
            "password": "senha"
        }

    def __dict__(self) -> dict:
        return {
            'cpf': self.cpf,
            'name': self.name,
            'phone': self.phone,
            'state': self.state,
            'city': self.state,
            'address': self.address,
            'number': self.number,
            'cep': self.cep,
            'birthdate': self.birthdate,
            'gender': self.gender,
            'email': self.email,
            'photo': self.photo,
            'animals': self.animals,
            'responses': self.responses,
            'created_at': self.created_at,
            'updated_at': datetime.now(),
            'password': self.password,
        }
    
    @staticmethod
    def adopter_helper(adopter) -> dict:
        return {
            "id": str(adopter["_id"]),
            "cpf": adopter["cpf"],
            "name": adopter["name"],
            "phone": adopter["phone"],
            "state": adopter["state"],
            "city": adopter["city"],
            "address": adopter["address"],
            "number": adopter["number"],
            "cep": adopter["cep"],
            "birthdate": adopter["birthdate"],
            "gender": adopter["gender"],
            "email": adopter["email"],
            "photo": adopter["photo"],
            "animals": adopter["animals"],
            "responses": adopter["responses"],
            "created_at": adopter["created_at"],
            "updated_at": adopter["updated_at"],
        }