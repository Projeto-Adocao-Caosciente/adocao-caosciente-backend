import bson
from datetime import datetime
from datetime import datetime
import bcrypt
from app.domain.models.animal import AnimalModel
from app.domain.models.ong import OngModel
from app.domain.database.db import Database


class OngService:
    def __init__(self):
        self.db = Database()
        self.ongs_collection = self.db.get_database().get_collection("ongs")

    def create_ong(self, ong: OngModel) -> bool:
        print(ong)
        try:
            with self.db.session.start_transaction():
                # FIXME: Encriptar senha de alguma forma, aqui dá erro -> 'OngModel' object has no attribute 'password'
                # salt = bcrypt.gensalt()  # definir rounds torna a operação mais lenta
                # ong.password = bcrypt.hashpw(
                ong.created_at = datetime.now()
                result = self.ongs_collection.insert_one(ong.dict())
                return True if result else False
        except Exception as e:
            print(f"Error creating ong: {e}")
            return False

    def update_ong(self, ong: OngModel, ong_email: str) -> bool:
        try:
            with self.db.session.start_transaction():
                # TODO: O update n funciona muito bem ainda, ajustar isso
                old_ong = self.get_ong_by_email(ong_email)
                
                # Create a dict of the fields that needs to be updated
                update_fields = {}
                
                for key, value in ong.dict().items():
                    # Update keys that is diferent from old data and is not empty, ignore _id, created at and updated_at
                    if key not in ["_id", "created_at", "updated_at"] and value != old_ong.get(key) and value:
                        update_fields[key] = value
                # if any field was modified 
                if update_fields:
                    #change value of updated_at to now
                    update_fields["updated_at"] = datetime.now()
                    result = self.ongs_collection.update_one(
                        {"email": ong_email},
                        {"$set": update_fields}
                    )
                return True if result else False
        except Exception as e:
            print(f"Error updating ong: {e}")
            return False

    def get_ong_by_email(self, ong_email: str):
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
    
    def update_ong_animals(self, ong_id, animal_id):
        try:
            with self.db.session.start_transaction():
                result = self.ongs_collection.update_one(
                    {"_id": bson.ObjectId(ong_id)},
                    {"$push": {"animals": animal_id}}
                )
                return True if result else False
        except Exception as e:
            print(f"Error updating ong animals: {e}")
            return False
