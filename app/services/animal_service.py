import time
from typing import Optional
from app.domain.models.animal import AnimalModel
from app.domain.database.db import Database
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult
from bson import ObjectId

from app.services.ong_service import OngService

class AnimalService:
    def __init__(self, ong_service: OngService):
        self.db = Database()
        self.ong_service = ong_service
        self.animals_collection = self.db.get_database().get_collection("animals")

    def create_animal(self, animal: AnimalModel) -> bool:
        try:
            with self.db.session.start_transaction():
                animal.created_at = time.time()
                result = self.animals_collection.insert_one(animal.dict())
                return True if isinstance(result, InsertOneResult) else False
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
                return True if isinstance(result, UpdateResult) else False
        except Exception as e:
            print(f"Error updating animal: {e}")
            return False

    def delete_animal(self, animal_id: str) -> bool:
        try:
            with self.db.session.start_transaction():
                # TODO: Deleção lógica
                result = self.animals_collection.delete_one({"_id": animal_id})
                return True if isinstance(result, DeleteResult) else False
        except Exception as e:
            print(f"Error deleting animal: {e}")
            return False
  
    def get_animal(self, animal_id: str, ong_email: str):
        try:
            ong = self.ong_service.get_ong(ong_email)
            # TODO: Se a ong não existir mais, não retornar o animal, isso ta certo?
            if ong is None:
                return None

            result = self.animals_collection.find_one({"_id": ObjectId(animal_id), "ong": ong["_id"]})
            return AnimalModel.animal_helper(result)
        except Exception as e:
            print(f"Error getting animal: {e}")
            return None