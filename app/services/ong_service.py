from app.domain.models.ong import OngModel
from app.domain.database.db import Database
from bson import ObjectId
from app.services.animal_service import AnimalService

class OngService:
    def __init__(self):
        self.db = Database()
        self.ongs_collection = self.db.get_database().get_collection("ongs")
    
    def create_ong(self, ong: OngModel) -> int:
        with self.db.session.start_transaction():
            result = self.ongs_collection.insert_one(ong.dict())
            return result.inserted_id
    
    # TODO: tratar erros
    def update_ong(self, ong: OngModel, ong_id: str) -> None:
        with self.db.session.start_transaction():
            self.ongs_collection.update_one(
                {"_id": ObjectId(ong_id)},
                {"$set": ong.dict()}
            )
    
    # TODO: Tratar erros
    def delete_ong(self, ong_id: str) -> None:
        # TODO: Deleção lógica
        with self.db.session.start_transaction():
            self.ongs_collection.delete_one({"_id": ong_id})
    
    def get_ong(self, ong_id: str):
        result = self.ongs_collection.find_one({"_id": ObjectId(ong_id)})
        return OngService.ong_helper(result)
    
    def get_ong_animals(self, ong_id: str) -> list:
        result = list(self.ongs_collection.aggregate([
            {
                "$match": {"_id": ObjectId(ong_id)}
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
                "$project": {
                    "animals": 1
                }
            }
        ]))
        if result:
            animals = result[0]["animals"]
            return [AnimalService.animal_helper(animal) for animal in animals]
        return []

    @staticmethod
    def ong_helper(ong) -> dict:
        return {
            "id": str(ong["_id"]),
            "name": ong["name"],
            "logo": ong["logo"],
            "city": ong["city"],
            "state": ong["state"],
            "phone": ong["phone"],
            "email": ong["email"],
            "mission": ong["mission"],
            "foundation": ong["foundation"],
            "description": ong["description"],    
        }