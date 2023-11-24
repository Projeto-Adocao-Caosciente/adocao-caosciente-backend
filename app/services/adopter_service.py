from datetime import datetime
from bson import ObjectId

from app.domain.database.db import Database
from app.domain.models.adopter import AdopterModel
from app.domain.models.animal import AnimalModel

class AdopterService:
    def __init__(self):
        self.db = Database()
        self.adopter_collection = self.db.get_database().get_collection("Adopter")

    def create_adopter(self, adopter: AdopterModel) -> bool:
        print(adopter)
        try:
            with self.db.session.start_transaction():
                adopter.create_at = datetime.now()
                result = self.adopter_collection.insert_one(adopter.dict())
                return True if result else False
        except Exception as e:
            print(f"Erro creating adopter: {e}")
            return False

    def get_adopter_by_id(self, adopter_id: str):
        try:
            result = self.adopter_collection.find_one({"_id": ObjectId(adopter_id)})
            if result:
                return AdopterModel.adopter_helper(result)
            return None
        except Exception as e:
            print(f"Error getting adopter: {e}")
            return None
        
    def get_adopter_by_cpf(self, cpf: str):
        try:
            result = self.adopter_collection.find_one({"cpf": cpf})
            if result:
                return result
            return None
        except Exception as e:
            print(f"Error getting adopter by cpf: {e}")
            return None
        
    def get_adopter_animals(self, adopter_id: str) -> list:
        try:
            result = list(self.adopter_collection.aggregate([
                {
                    "$match": {"_id": ObjectId(adopter_id)}
                },
                {
                    "$lookup": {
                        "from": "animals",
                        "localField": "animals",
                        "foreignField": "_id",
                        "as": "animals"
                    }
                },
                {
                    "$sort": {"animals.created_at": -1, "animals.name": 1}
                },
                {
                    "$project": {
                        "animals": 1
                    }
                }
            ]))
            if result:
                animals = result[0]["animals"]
                return [AnimalModel.animal_helper(animal) for animal in animals]
            return []
        except Exception as e:
            print(f"Error getting ong animals: {e}")
            return []
        
    def update_adopter_animals(self, adopter_id, animal_id):
        try:
            with self.db.session.start_transaction():
                result = self.adopter_collection.update_one(
                    {"_id": ObjectId(adopter_id)},
                    {"$push": {"animals": animal_id}}
                )
                return True if result else False
        except Exception as e:
            print(f"Error updating adopter animals: {e}")
            return False
        