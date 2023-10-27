import bcrypt
from app.domain.models.animal import AnimalModel
from app.domain.models.ong import OngModel
from app.domain.database.db import Database
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult

class OngService:
    def __init__(self):
        self.db = Database()
        self.ongs_collection = self.db.get_database().get_collection("ongs")
    

    def create_ong(self, ong: OngModel) -> bool:
        try:
            with self.db.session.start_transaction():
                salt = bcrypt.gensalt() # definir rounds torna a operação mais lenta
                ong.password = bcrypt.hashpw(ong.password.encode(), salt)
                result = self.ongs_collection.insert_one(ong.dict())                
                return True if isinstance(result, InsertOneResult) else False
        except Exception as e:
            print(f"Error creating ong: {e}")
            return False
    
    def update_ong(self, ong: OngModel, ong_email: str) -> bool:
        try:
            with self.db.session.start_transaction():
                result = self.ongs_collection.update_one(
                    {"email": ong_email},
                    {"$set": ong.dict()}
                )
                return True if isinstance(result, UpdateResult) else False
        except Exception as e:
            print(f"Error updating ong: {e}")
            return False
    
    def delete_ong(self, ong_email: str) -> bool:
        try:
            with self.db.session.start_transaction():
                # TODO: Deleção lógica
                result = self.ongs_collection.delete_one({"email": ong_email})
                return True if isinstance(result, DeleteResult) else False
        except Exception as e:
            print(f"Error deleting ong: {e}")
            return False

    def get_ong(self, ong_email: str):
        try:
            result = self.ongs_collection.find_one({"email": ong_email})
            if result:
                return OngModel.ong_helper(result)
            return None
        except Exception as e:
            print(f"Error getting ong: {e}")
            return None
    
    def get_ong_by_cnpj(self, cnpj: str):
        try:
            result = self.ongs_collection.find_one({"cnpj": cnpj})
            if result:
                return result
            return None
        except Exception as e:
            print(f"Error getting ong by cnpj: {e}")
            return None

    def get_ong_animals(self, ong_email: str) -> list:
        try:
            result = list(self.ongs_collection.aggregate([
                {
                    "$match": {"email": ong_email}
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
                return [AnimalModel.animal_helper(animal) for animal in animals]
            return []
        except Exception as e:
            print(f"Error getting ong animals: {e}")
            return []
    