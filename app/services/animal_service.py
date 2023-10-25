from app.domain.models.animal import AnimalModel
from app.domain.database.db import Database
from bson import ObjectId

class AnimalService:
    def __init__(self):
        self.db = Database()
        self.animals_collection = self.db.get_database().get_collection("animals")

    def create_animal(self, animal: AnimalModel) -> int:
        with self.db.session.start_transaction():
            result = self.animals_collection.insert_one(animal)
            return result.inserted_id

    # TODO: tratar erros
    def update_animal(self, animal: AnimalModel, animal_id: str) -> None:
        with self.db.session.start_transaction():
            self.animals_collection.update_one(
                {"_id": ObjectId(animal_id)},
                {"$set": animal.dict()}
            )
            
    # TODO: tratar erros
    def delete_animal(self, animal_id: str) -> None:
        # TODO: Deleção lógica
       with self.db.session.start_transaction():
            self.animals_collection.delete_one({"_id": animal_id})
  
    def get_animal(self, animal_id: str):
        result = self.animals_collection.find_one({"_id": ObjectId(animal_id)})
        return AnimalService.animal_helper(result)

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