import bycrypt
from app.domain.models.ong import OngModel
from app.domain.database.db import Database
from bson import ObjectId
from pymongo.results import InsertOneResult
from app.services.animal_service import AnimalService

class OngService:
    def __init__(self):
        self.db = Database()
        self.ongs_collection = self.db.get_database().get_collection("ongs")
    

    def create_ong(self, ong: OngModel) -> bool:
        try:
            with self.db.session.start_transaction():
                salt = bycrypt.gensalt() # definir rounds torna a operação mais lenta
                ong.password = bycrypt.hashpw(ong.password.encode(), salt)
                result = self.ongs_collection.insert_one(ong.model_dump())                
                return True if isinstance(result, InsertOneResult) else False
        except Exception as e:
            print(f"Error creating ong: {e}")
            return False
    
    def update_ong(self, ong: OngModel, ong_id: str) -> bool:
        try:
            with self.db.session.start_transaction():
                self.ongs_collection.update_one(
                    {"_id": ObjectId(ong_id)},
                    {"$set": ong.model_dump()}
                )
                return True
        except Exception as e:
            print(f"Error updating ong: {e}")
            return False
    
    def delete_ong(self, ong_id: str) -> bool:
        try:
            with self.db.session.start_transaction():
                # TODO: Deleção lógica
                result = self.ongs_collection.delete_one({"_id": ObjectId(ong_id)})
                return True if result.deleted_count > 0 else False
        except Exception as e:
            print(f"Error deleting ong: {e}")
            return False

    def get_ong(self, ong_id: str):
        try:
            result = self.ongs_collection.find_one({"_id": ObjectId(ong_id)})
            if result:
                return OngService.ong_helper(result)
            return None
        except Exception as e:
            print(f"Error getting ong: {e}")
            return None
    
    def get_ong_by_cnpj(self, cnpj: str):
        try:
            result = self.ongs_collection.find_one({"cnpj": cnpj})
            if result:
                return {"email": result["email"], "password": result["password"]}
            return None
        except Exception as e:
            print(f"Error getting ong by cnpj: {e}")
            return None

    def get_ong_animals(self, ong_id: str) -> list:
        try:
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
        except Exception as e:
            print(f"Error getting ong animals: {e}")
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