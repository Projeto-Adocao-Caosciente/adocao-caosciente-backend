from datetime import datetime
from bson import ObjectId
import http
import logging
from pymongo.errors import DuplicateKeyError

from app.domain.database.db import Database
from app.domain.models.adopter import AdopterModel
from app.domain.models.animal import AnimalModel
from app.domain.models.dto.response import ResponseDTO, duplicate_key_response
from app.domain.models.roles import Role


class AdopterService:
    def __init__(self):
        self.db = Database()
        self.adopter_collection = self.db.get_database().get_collection("adopter")
        self.logger = logging.getLogger(__name__)

    def create_adopter(self, adopter: AdopterModel, request_id = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                current_time = datetime.now().isoformat()
                adopter.created_at = current_time
                adopter.updated_at = current_time
                result = self.adopter_collection.insert_one(adopter.model_dump())
                if result:
                    self.logger.info(f"id={request_id} Adopter created successfully")
                    return ResponseDTO({"id": str(result.inserted_id)}, "Adopter created successfully", http.HTTPStatus.CREATED)
                else:
                    self.logger.error(f"id={request_id} Error on create adopter")
                    return ResponseDTO(None, "Error on create adopter", http.HTTPStatus.BAD_REQUEST)
        except DuplicateKeyError as e:
            self.logger.error(f"id={request_id} Error creating adopter: {e}")
            duplicated_field = str(e).split("index: ")[1].split("_")[0]
            return duplicate_key_response(duplicated_field, AdopterModel.match_field)
        except Exception as e:
            self.logger.error(f"id={request_id} Error creating adopter: {e}")
            return ResponseDTO(None, "Error on create adopter", http.HTTPStatus.BAD_REQUEST)

    def update_adopter(self, adopter: AdopterModel, adopter_id: str, request_id = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                old_adopter = self.adopter_collection.find_one({"_id": ObjectId(adopter_id)})
                if not old_adopter:
                    self.logger.info(f"id={request_id} Adopter not found")
                    return ResponseDTO(None, "Adopter not found", http.HTTPStatus.NOT_FOUND)
                update_fields = { field : value for field, value in adopter.model_dump().items() if value != old_adopter[field] and value is not None }
                if len(update_fields) == 0:
                    self.logger.info(f"id={request_id} Adopter not modified")
                    return ResponseDTO(None, "Adopter not modified", http.HTTPStatus.OK)
                
                if "password" in update_fields:
                    self.logger.error(f"id={request_id} Password cannot be updated")
                    return ResponseDTO(None, "Password cannot be updated", http.HTTPStatus.BAD_REQUEST)
                
                current_time = datetime.now().isoformat()
                adopter.updated_at = current_time
                result = self.adopter_collection.update_one(
                    {"_id": ObjectId(adopter_id)}, 
                    {"$set": adopter.model_dump()}
                )
                if result:
                    self.logger.info(f"id={request_id} Adopter updated successfully")
                    return ResponseDTO({"id": str(adopter_id)}, "Adopter updated successfully", http.HTTPStatus.OK)
                self.logger.error(f"id={request_id} Error on update adopter")
                return ResponseDTO(None, "Error on update adopter", http.HTTPStatus.BAD_REQUEST)
        except DuplicateKeyError as e:
            self.logger.error(f"id={request_id} Error updating adopter: {e}")
            duplicated_field = str(e).split("index: ")[1].split("_")[0]
            return duplicate_key_response(duplicated_field, AdopterModel.match_field)
        except Exception as e:
            self.logger.error(f"id={request_id} Error updating adopter: {e}")
            return ResponseDTO(None, "Error on update adopter", http.HTTPStatus.BAD_REQUEST)


    def get_adopter_by_id(self, adopter_id: str, request_id = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            result = self.adopter_collection.find_one({"_id": ObjectId(adopter_id)})
            if result:
                self.logger.info(f"id={request_id} Adopter retrieved successfully")
                return ResponseDTO({"type": Role.USER, "user": AdopterModel.helper(result)}, "Adopter retrieved successfully", http.HTTPStatus.OK)
            self.logger.info(f"id={request_id} Adopter not found")
            return ResponseDTO(None, "Adopter not found", http.HTTPStatus.NOT_FOUND)
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting adopter: {e}")
            return ResponseDTO(None, "Error getting adopter", http.HTTPStatus.BAD_REQUEST)
        
    def get_adopter_by_cpf(self, cpf: str, request_id = ""):
        self.logger.info(f"id={request_id} Start service")
        try:
            result = self.adopter_collection.find_one({"cpf": cpf})
            if result:
                return result
            return None
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting adopter by cpf: {e}")
            return None
        
    def get_adopter_animals(self, adopter_id: str, request_id = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            response = self.get_adopter_by_id(adopter_id)
            if response.status != http.HTTPStatus.OK:
                return response
            
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
                self.logger.info(f"id={request_id} Adopter animals retrieved successfully")
                animals = [AnimalModel.helper(animal) for animal in result[0]["animals"]]
                return ResponseDTO(animals, "Adopter animals retrieved successfully", http.HTTPStatus.OK)
            self.logger.info(f"id={request_id} Adopter has no animals")
            return ResponseDTO([], "Adopter has no animals", http.HTTPStatus.OK)
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting adopter animals: {e}")
            return ResponseDTO(None, "Error on get adopter animals", http.HTTPStatus.BAD_REQUEST)