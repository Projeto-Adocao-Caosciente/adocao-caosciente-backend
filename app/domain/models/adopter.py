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
    animal: List[str] =  []
    responses: List[str] = []
    created_at: str = ""
    updated_at: str = datetime.now()

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
            "animal": adopter["animal"],
            "responses": adopter["responses"],
            "created_at": adopter["created_at"],
            "updated_at": adopter["updated_at"],
        }