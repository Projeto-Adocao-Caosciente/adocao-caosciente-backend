from app.domain.models.animal import AnimalModel
from app.domain.database.db import Database
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult
from bson import ObjectId

class AnimalService:
    def __init__(self):
        self.db = Database()
        self.animals_collection = self.db.get_database().get_collection("animals")

    def create_animal(self, animal: AnimalModel) -> bool:
        try:
            with self.db.session.start_transaction():
                result = self.animals_collection.insert_one(animal)
                return True if isinstance(result, InsertOneResult) else False
        except Exception as e:
            print(f"Error creating animal: {e}")
            return False

    def update_animal(self, animal: AnimalModel, animal_id: str) -> bool:
        try:
            with self.db.session.start_transaction():
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
                result = self.animals_collection.delete_one({"_id": animal_id})
                return True if isinstance(result, DeleteResult) else False
        except Exception as e:
            print(f"Error deleting animal: {e}")
            return False
  
    def get_animal(self, animal_id: str):
        try:
            result = self.animals_collection.find_one({"_id": ObjectId(animal_id)})
            return AnimalService.animal_helper(result)
        except Exception as e:
            print(f"Error getting animal: {e}")
            return None

    @staticmethod
    def animal_helper(animal) -> dict:
        return {
            "id": str(animal["_id"]),
            "ong": animal["ong"],
            "name": animal["name"],
            "type": animal["type"],
            "breed": animal["breed"],
            "height": animal["height"],
            "weight": animal["weight"],
            "special_needs": animal["special_needs"],
            "adoption_requirements": animal["adoption_requirements"],
            "photo": animal["photo"],
            "adopter": animal["adopter"],
        }