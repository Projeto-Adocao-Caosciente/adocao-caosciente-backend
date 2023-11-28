from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class AdopterModel(BaseModel):
    cpf: str = Field(None, min_length=11, max_length=11)
    name: str = Field(None, min_length=2, max_length=60)
    phone: str = Field(None, min_length=10, max_length=12)
    city: str = Field(None, min_length=2, max_length=60)
    state: str = Field(None, min_length=2, max_length=60)
    address: str = Field(None, min_length=2, max_length=60)
    cep: str = Field(None, min_length=8, max_length=8)
    birthdate: str = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
    gender: str = Field(None, min_length=2, max_length=60)
    email: str = Field(None, max_length=60)
    photo: str = Field(None, )
    animals: List[str] = Field([], )
    responses: List[str] = Field([], )
    created_at: str = Field(None, )
    updated_at: str = datetime.now().isoformat()
    password: str = Field(None, min_length=4, max_length=60)

    class Config:
        json_schema_extra = {
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
    def helper(adopter) -> dict:
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
        
    def remove_mask_cpf(self):
        cpf_normalized = self.model_dump()["cpf"].replace(".", "").replace("-", "")
        self.cpf = cpf_normalized
        
    def remove_mask_cep(self):
        cep_normalized = self.model_dump()["cep"].replace(".", "").replace("-", "")
        self.cep = cep_normalized
        
    def remove_mask_phone(self):
        phone_normalized = self.model_dump()["phone"].replace("(", "").replace(")", "").replace(" ", "").replace(".", "").replace("/", "").replace("-", "")
        self.phone = phone_normalized