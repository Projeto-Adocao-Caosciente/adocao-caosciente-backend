from bson import ObjectId
from datetime import datetime
import bcrypt
from app.domain.models.animal import AnimalModel
from app.domain.models.ong import OngModel
from app.domain.database.db import Database
import http
from app.domain.models.dto.response import ResponseDTO

class OngService:
    def __init__(self):
        self.db = Database()
        self.ongs_collection = self.db.get_database().get_collection("ongs")

    def create_ong(self, ong: OngModel) -> ResponseDTO:
        try:
            with self.db.session.start_transaction():
                # FIXME: Encriptar senha de alguma forma, aqui dá erro -> 'OngModel' object has no attribute 'password'
                # salt = bcrypt.gensalt()  # definir rounds torna a operação mais lenta
                # ong.password = bcrypt.hashpw(
                current_time = datetime.now().isoformat()
                ong.created_at = current_time
                ong.updated_at = current_time
                result = self.ongs_collection.insert_one(ong.model_dump())
                if result:
                    return ResponseDTO({"id": str(result.inserted_id)}, "Ong created successfully", http.HTTPStatus.CREATED)
                else:
                    return ResponseDTO(None, "Error on create", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            print(f"Error creating ong: {e}")
            return ResponseDTO(None, "Error on create ong", http.HTTPStatus.BAD_REQUEST)

    def update_ong(self, ong: OngModel, ong_id: str) -> ResponseDTO:
        try:
            with self.db.session.start_transaction():
                old_ong = self.ongs_collection.find_one({"_id": ObjectId(ong_id)})

                if not old_ong:
                    return ResponseDTO(None, "Ong not found", http.HTTPStatus.NOT_FOUND)
                update_fields = { field : value for field, value in ong.model_dump().items() if value != old_ong[field] and value is not None }
                if len(update_fields) == 0:
                    return ResponseDTO(None, "Ong not modified", http.HTTPStatus.OK)
                
                if "password" in update_fields:
                    return ResponseDTO(None, "Password cannot be updated", http.HTTPStatus.BAD_REQUEST)

                # Check if email or cnpj is already in use
                if "email" in update_fields:
                    ong = self.ongs_collection.find_one({"email": update_fields["email"]})
                    if ong:
                        return ResponseDTO(None, "Email already in use", http.HTTPStatus.BAD_REQUEST)
                if "cnpj" in update_fields:
                    ong = self.ongs_collection.find_one({"cnpj": update_fields["cnpj"]})
                    if ong:
                        return ResponseDTO(None, "CNPJ already in use", http.HTTPStatus.BAD_REQUEST)
                
                update_fields["updated_at"] = datetime.now().isoformat()
                result = self.ongs_collection.update_one(
                    {"_id": ObjectId(ong_id)},
                    {"$set": update_fields}
                )
                if result:
                    return ResponseDTO(None, "Ong updated successfully", http.HTTPStatus.OK)
                else:
                    return ResponseDTO(None, "Error on update ong", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            print(f"Error updating ong: {e}")
            return ResponseDTO(None, "Error on update ong", http.HTTPStatus.BAD_REQUEST)

    def delete_ong(self, ong_id: str) -> bool:
        try:
            with self.db.session.start_transaction():
                deleted_ongs = self.db.get_database().get_collection("deleted_ongs")
                # Verifica se o array ong.animals está vazio
                
                animals = self.get_ong_animals(ong_id)
                if not animals:
                    ong = self.ongs_collection.find_one({"_id": ObjectId(ong_id)})
                    result = deleted_ongs.insert_one(ong)
                    if result:
                        result = self.ongs_collection.delete_one({"_id": ObjectId(ong_id)})
                    return True if result else False

                # Se o array ong.animals não estiver vazio, retorna False
                return False

        except Exception as e:
            print(f"Error deleting ong: {e}")
            return False

    def get_ong_by_id(self, ong_id: str) -> ResponseDTO:
        try:
            result = self.ongs_collection.find_one({"_id": ObjectId(ong_id)})
            if result:
                return ResponseDTO(OngModel.helper(result), "Ong retrieved successfully", http.HTTPStatus.OK)
            return ResponseDTO(None, "Ong not found", http.HTTPStatus.NOT_FOUND)
        except Exception as e:
            print(f"Error getting ong: {e}")
            return ResponseDTO(None, "Error on get ong by id", http.HTTPStatus.BAD_REQUEST)

    def get_ong_by_cnpj(self, cnpj: str):
        try:
            result = self.ongs_collection.find_one({"cnpj": cnpj})
            if result:
                return result
            return None
        except Exception as e:
            print(f"Error getting ong by cnpj: {e}")
            return None

    def get_ong_animals(self, ong_id: str) -> ResponseDTO:
        try:
            response = self.get_ong_by_id(ong_id)
            if response.status != http.HTTPStatus.OK:
                return response
        
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
                    "$sort": {"animals.created_at": -1, "animals.name": 1}
                },
                {
                    "$project": {
                        "animals": 1
                    }
                }
            ]))
            if result:
                animals = [AnimalModel.animal_helper(animal) for animal in result[0]["animals"]]
                return ResponseDTO(animals, "Ong animals retrieved successfully", http.HTTPStatus.OK)
            return ResponseDTO([], "Ong has no animals", http.HTTPStatus.OK)
        except Exception as e:
            print(f"Error getting ong animals: {e}")
            return ResponseDTO(None, "Error on get ong animals", http.HTTPStatus.BAD_REQUEST)
    
    def update_ong_animals(self, ong_id, animal_id) -> ResponseDTO:
        try:
            with self.db.session.start_transaction():
                result = self.ongs_collection.update_one(
                    {"_id": ObjectId(ong_id)},
                    {"$push": {"animals": animal_id}}
                )
                if result:
                    return ResponseDTO(None, "Ong animals updated successfully", http.HTTPStatus.OK)
                else:
                    return ResponseDTO(None, "Error on update ong animals", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            print(f"Error updating ong animals: {e}")
            return ResponseDTO(None, "Error on update ong animals", http.HTTPStatus.BAD_REQUEST)