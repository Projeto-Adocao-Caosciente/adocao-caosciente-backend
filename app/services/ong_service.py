import logging
import re
import unicodedata
from bson import ObjectId
from datetime import datetime
import bcrypt
from app.domain.models.animal import AnimalModel
from app.domain.models.ong import OngModel
from app.domain.database.db import Database
import http
from app.domain.models.dto.response import duplicate_key_response, ResponseDTO
from pymongo.errors import DuplicateKeyError
from app.domain.models.roles import Role

from Levenshtein import distance as levenshtein_distance

from utils.util import Util

class OngService:
    def __init__(self):
        self.db = Database()
        self.ongs_collection = self.db.get_database().get_collection("ongs")
        self.logger = logging.getLogger(__name__)

    def create_ong(self, ong: OngModel,  request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                # FIXME: Adicionar encriptação de senha
                current_time = datetime.now().isoformat()
                ong.created_at = current_time
                ong.updated_at = current_time
                result = self.ongs_collection.insert_one(ong.model_dump())
                if result:
                    self.logger.info(f"id={request_id} Ong created successfully")
                    return ResponseDTO({"id": str(result.inserted_id)}, "Ong created successfully", http.HTTPStatus.CREATED)
                else:
                    self.logger.error(f"id={request_id} Error on create ong")
                    return ResponseDTO(None, "Error on create ong", http.HTTPStatus.BAD_REQUEST)
        except DuplicateKeyError as e:
            self.logger.error(f"id={request_id} Error on create ong: {e}")
            duplicated_field = str(e).split("index: ")[1].split("_")[0]
            return duplicate_key_response(duplicated_field, OngModel.match_field)
        except Exception as e:
            self.logger.error(f"id={request_id} Error creating ong: {e}")
            return ResponseDTO(None, "Error on create ong", http.HTTPStatus.BAD_REQUEST)
        

    def update_ong(self, ong: OngModel, ong_id: str,  request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                old_ong = self.ongs_collection.find_one({"_id": ObjectId(ong_id)})

                if not old_ong:
                    self.logger.error(f"id={request_id} Ong not found")
                    return ResponseDTO(None, "Ong not found", http.HTTPStatus.NOT_FOUND)
                update_fields = { field : value for field, value in ong.model_dump().items() if value != old_ong[field] and value is not None }
                if len(update_fields) == 0:
                    self.logger.info(f"id={request_id} Ong not modified")
                    return ResponseDTO(None, "Ong not modified", http.HTTPStatus.OK)
                
                if "password" in update_fields:
                    self.logger.error(f"id={request_id} Password cannot be updated")
                    return ResponseDTO(None, "Password cannot be updated", http.HTTPStatus.BAD_REQUEST)
                
                update_fields["updated_at"] = datetime.now().isoformat()
                result = self.ongs_collection.update_one(
                    {"_id": ObjectId(ong_id)},
                    {"$set": update_fields}
                )
                if result:
                    self.logger.info(f"id={request_id} Ong updated successfully")
                    return ResponseDTO(None, "Ong updated successfully", http.HTTPStatus.OK)
                else:
                    self.logger.error(f"id={request_id} Error on update ong")
                    return ResponseDTO(None, "Error on update ong", http.HTTPStatus.BAD_REQUEST)
        except DuplicateKeyError as e:
            self.logger.error(f"id={request_id} Error on update ong: {e}")
            duplicated_field = str(e).split("index: ")[1].split("_")[0]
            return duplicate_key_response(duplicated_field, OngModel.match_field)
        except Exception as e:
            self.logger.error(f"id={request_id} Error updating ong: {e}")
            return ResponseDTO(None, "Error on update ong", http.HTTPStatus.BAD_REQUEST)

    def delete_ong(self, ong_id: str, request_id: str = "") -> bool:
        try:
            with self.db.session.start_transaction():
                deleted_ongs = self.db.get_database().get_collection("deleted_ongs")
                
                animals = self.get_ong_animals(ong_id)
                if not animals:
                    ong = self.ongs_collection.find_one({"_id": ObjectId(ong_id)})
                    result = deleted_ongs.insert_one(ong)
                    if result:
                        result = self.ongs_collection.delete_one({"_id": ObjectId(ong_id)})
                    return True if result else False

                return False

        except Exception as e:
            self.logger.error(f"id={request_id} Error deleting ong: {e}")
            return False

    def get_ong_by_id(self, ong_id: str, request_id=None) -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            result = self.ongs_collection.find_one({"_id": ObjectId(ong_id)})
            if result:
                self.logger.info(f"id={request_id} Ong retrieved successfully")
                return ResponseDTO({"type": Role.ONG, "user": OngModel.helper(result)}, "Ong retrieved successfully", http.HTTPStatus.OK)
            self.logger.info(f"id={request_id} Ong not found")
            return ResponseDTO(None, "Ong not found", http.HTTPStatus.NOT_FOUND)
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting ong: {e}")
            return ResponseDTO(None, "Error on get ong by id", http.HTTPStatus.BAD_REQUEST)

    def get_ong_by_cnpj(self, cnpj: str, request_id: str = ""):
        try:
            result = self.ongs_collection.find_one({"cnpj": cnpj})
            if result:
                return result
            return None
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting ong by cnpj: {e}")
            return None

    def get_ong_animals(self, ong_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            response = self.get_ong_by_id(ong_id, request_id)
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
                    "$unwind": "$animals"
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
                animals = [AnimalModel.helper(animal['animals']) for animal in result]
                self.logger.info(f"id={request_id} Ong animals retrieved successfully")
                return ResponseDTO(animals, "Ong animals retrieved successfully", http.HTTPStatus.OK)
            self.logger.info(f"id={request_id} Ong has no animals")
            return ResponseDTO([], "Ong has no animals", http.HTTPStatus.OK)
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting ong animals: {e}")
            return ResponseDTO(None, "Error on get ong animals", http.HTTPStatus.BAD_REQUEST)
    
    def get_ong_animals_by_name(self, name: str, ong_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                ong_animals = self.get_ong_animals(ong_id, request_id)
                if ong_animals.status != http.HTTPStatus.OK:
                    return ong_animals
                
                # Normalize name
                name = name.lower()
                name = Util.remove_accents(name)

                # Normalize animals names
                animals = ong_animals.data
                normalized_animals_names = [Util.remove_accents(animal['name'].lower()) for animal in animals]

                # Filter by name
                filtered_animals = []
                THRESHOLD = 3
                for idx, normalized_animal_name in enumerate(normalized_animals_names):
                    if name in normalized_animal_name or levenshtein_distance(normalized_animal_name, name) <= THRESHOLD:
                        filtered_animals.append(animals[idx])

                if not filtered_animals:
                    self.logger.info(f"id={request_id} Ong has no animals with a similar name")
                    return ResponseDTO([], "Ong has no animals with a similar name", http.HTTPStatus.OK)
                
                # Sort by similiarity with name
                # NOTE: the levenshtein_distance is not a good metric for this, but it's the best we have for now
                # TODO: find a better way to sort by similarity
                # the names already have accents removed, so we don't need to remove them again
                filtered_animals.sort(key=lambda animal: levenshtein_distance(animal['name'].lower(), name))

                self.logger.info(f"id={request_id} Ong animals retrieved successfully")
                return ResponseDTO(filtered_animals, "Ong animals retrieved successfully", http.HTTPStatus.OK)
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting animal: {e}")
            return ResponseDTO(None, "Error on get animal", http.HTTPStatus.BAD_REQUEST)

    def update_ong_animals(self, ong_id, animal_id,  request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                result = self.ongs_collection.update_one(
                    {"_id": ObjectId(ong_id)},
                    {"$push": {"animals": animal_id}}
                )
                if result:
                    self.logger.info(f"id={request_id} Ong animals updated successfully")
                    return ResponseDTO(None, "Ong animals updated successfully", http.HTTPStatus.OK)
                else:
                    self.logger.error(f"id={request_id} Error on update ong animals")
                    return ResponseDTO(None, "Error on update ong animals", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"id={request_id} Error updating ong animals: {e}")
            return ResponseDTO(None, "Error on update ong animals", http.HTTPStatus.BAD_REQUEST)