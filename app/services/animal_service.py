from datetime import datetime
import http
import fastapi
from typing import Optional
from app.domain.models.animal import AnimalModel
from app.domain.database.db import Database
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult
from bson import ObjectId
from app.domain.models.dto.response import ResponseDTO


from app.services.ong_service import OngService

class AnimalService:
    def __init__(self, ong_service: OngService):
        self.db = Database()
        self.ong_service = ong_service
        self.animals_collection = self.db.get_database().get_collection("animals")

    def create_animal(self, animal: AnimalModel, ong_id: str) -> bool:
        try:
            with self.db.session.start_transaction():
                animal.created_at = datetime.now()
                result = self.animals_collection.insert_one(animal.dict())
                if result == False:
                    raise fastapi.HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="Error creating animal.")
                ong = self.ong_service.get_ong_by_id(ong_id)
                if ong is None:
                    raise fastapi.HTTPException(status_code=http.HTTPStatus.BAD_REQUEST, detail="Ong not found.")
                result = self.ong_service.update_ong_animals(ong["id"], result.inserted_id)
                return True if result else False
        except Exception as e:
            print(f"Error creating animal: {e}")
            return False

    def update_animal(self, animal: AnimalModel, animal_id: str) -> bool:
        try:
            with self.db.session.start_transaction():
                # TODO: O update n funciona muito bem ainda, ajustar isso
                result = self.animals_collection.update_one(
                    {"_id": ObjectId(animal_id)},
                    {"$set": animal.dict()}
                )
                return True if result else False
        except Exception as e:
            print(f"Error updating animal: {e}")
            return False

    def delete_animal(self, animal_id: str) -> bool:
        try:
            with self.db.session.start_transaction():
                # TODO: Deleção lógica
                result = self.animals_collection.delete_one({"_id": ObjectId(animal_id)})
                return True if result else False
        except Exception as e:
            print(f"Error deleting animal: {e}")
            return False

    def get_animal(self, animal_id: str, ong_id: str):
        try:
            ong = self.ong_service.get_ong_by_id(ong_id)
            # TODO: Se a ong não existir mais, não retornar o animal, isso ta certo?
            if ong is None:
                return None

            result = self.animals_collection.find_one(
                {"_id": ObjectId(animal_id), "ong": ong["cnpj"]})
            return AnimalModel.animal_helper(result)
        except Exception as e:
            print(f"Error getting animal: {e}")
            return None
    
    def insert_form(self, animal_id: str, form_id: str) -> ResponseDTO:
        try:
            with self.db.session.start_transaction():
                result = self.animals_collection.update_one(
                    {"_id": ObjectId(animal_id)},
                    {"$push": {"forms": form_id}}
                )
                if result:
                    return ResponseDTO(http.HTTPStatus.OK, "Form inserted", result)
                else:
                    return ResponseDTO(http.HTTPStatus.BAD_REQUEST, "Could not insert form", None)
        except Exception as e:
            msg = f"Error updating ong animals: {e}"
            print(msg)
            return ResponseDTO(http.HTTPStatus.BAD_REQUEST, msg, None)
