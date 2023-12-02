from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
import re

from utils.mask import Mask

class AdopterModel(BaseModel):
    cpf: str = Field(None, pattern=Mask.CPF)
    name: str = Field(None, min_length=2, max_length=60)
    phone: str = Field(None, pattern=Mask.PHONE)
    city: str = Field(None, min_length=2, max_length=60)
    state: str = Field(None, min_length=2, max_length=60)
    address: str = Field(None, min_length=2, max_length=60)
    cep: str = Field(None, pattern=Mask.CEP)
    birthdate: str = Field(None, pattern=Mask.DATE)
    gender: str = Field(None, min_length=2, max_length=60)
    email: str = Field(None, max_length=60)
    photo: str = Field(None, )
    animals: List[str] = Field([], )
    responses: List[str] = Field([], )
    created_at: str = Field(None, )
    updated_at: str = datetime.now().isoformat()
    password: str = Field(None, min_length=4, max_length=60)

    def required_field_at_create(self) -> set:
        return {"cpf", "name", "phone", "city", "state", "address", "cep", "birthdate", "gender", "email", "photo", "password" }

    class Config:
        json_schema_extra = {
            "cpf": "12345678901",
            "name": "Adopter Name",
            "phone": "(11) 98765-4321",
            "state": "ST",
            "city": "City Name",
            "address": "Address Name",
            "cep": "12345-678",
            "birthdate": "2003-01-01",
            "gender": "Masculine",
            "email": "adopter@gmail.com",
            "password": "your_password"
        }

    def __dict__(self) -> dict:
        return {
            'cpf': self.cpf,
            'name': self.name,
            'phone': self.phone,
            'state': self.state,
            'city': self.state,
            'address': self.address,
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
    def helper(adopter) -> dict:
        return {
            "id": str(adopter["_id"]),
            "cpf": adopter["cpf"],
            "name": adopter["name"],
            "phone": adopter["phone"],
            "state": adopter["state"],
            "city": adopter["city"],
            "address": adopter["address"],
            "cep": adopter["cep"],
            "birthdate": adopter["birthdate"],
            "gender": adopter["gender"],
            "email": adopter["email"],
            "photo": adopter["photo"],
            "created_at": adopter["created_at"],
            "updated_at": adopter["updated_at"],
        }
    
    @staticmethod
    def match_field(field):
        real_field_name = {
            "cpf": "CPF",
            "name": "Nome",
            "phone": "Telefone",
            "state": "Estado",
            "city": "Cidade",
            "address": "Endereço",
            "cep": "CEP",
            "birthdate": "Data de nascimento",
            "gender": "Gênero",
            "email": "E-mail",
            "password": "Senha",
        }
        return real_field_name[field]

    def remove_mask_cpf(self) -> None:
        if self.model_dump()['cpf'] is None:
            return
        self.cpf = self.remove_non_digits(self.model_dump()["cpf"])

    def remove_mask_cep(self) -> None:
        if self.model_dump()['cep'] is None:
            return
        self.cep = self.remove_non_digits(self.model_dump()["cep"])

    def remove_mask_phone(self) -> None:
        if self.model_dump()['phone'] is None:
            return
        self.phone = self.remove_non_digits(self.model_dump()["phone"])
    
    def remove_non_digits(self, value):
        return re.sub(r'\D', '', value)