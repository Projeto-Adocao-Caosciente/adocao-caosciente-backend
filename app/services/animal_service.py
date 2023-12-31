from datetime import datetime
import http
import logging
from app.domain.models.animal import AnimalModel
from app.domain.database.db import Database
from bson import ObjectId
from app.domain.models.dto.response import ResponseDTO

from app.services.ong_service import OngService

class AnimalService:
    def __init__(self, ong_service: OngService):
        self.db = Database()
        self.ong_service = ong_service
        self.animals_collection = self.db.get_database().get_collection("animals")
        self.logger = logging.getLogger(__name__)

    def create_animal(self, animal: AnimalModel, ong_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                current_time = datetime.now().isoformat()
                animal.created_at = current_time
                animal.updated_at = current_time

                response = self.ong_service.get_ong_by_id(ong_id, request_id)
                if response.status != http.HTTPStatus.OK:
                    self.logger.error(f"id={request_id} Error creating animal: {response.message}")
                    return response

                ong_id = response.data['user']['id']

                result = self.animals_collection.insert_one(animal.model_dump())
                if not result:
                    self.logger.error(f"id={request_id} Error on create animal")
                    return ResponseDTO(None, "Error on create animal", http.HTTPStatus.BAD_REQUEST)
                
                response = self.ong_service.update_ong_animals(ong_id, result.inserted_id, request_id)
                if response.status != http.HTTPStatus.OK:
                    return response
                
                self.logger.info(f"id={request_id} Animal created successfully")
                return ResponseDTO({"id": str(result.inserted_id)}, "Animal created successfully", http.HTTPStatus.CREATED)
        except Exception as e:
            self.logger.error(f"id={request_id} Error creating animal: {e}")
            return ResponseDTO(None, "Error on create animal", http.HTTPStatus.BAD_REQUEST)

    def update_animal(self, animal: AnimalModel, animal_id: str, ong_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                old_animal = self.animals_collection.find_one({"_id": ObjectId(animal_id)})
                if not old_animal:
                    self.logger.info(f"id={request_id} Animal not found")
                    return ResponseDTO(None, "Animal not found", http.HTTPStatus.NOT_FOUND)

                update_fields = { field : value for field, value in animal.model_dump().items() if value != old_animal[field] and value is not None }
                if len(update_fields) == 0:
                    self.logger.info(f"id={request_id} Animal not modified")
                    return ResponseDTO(None, "Animal not modified", http.HTTPStatus.OK)

                animal.updated_at = datetime.now().isoformat()
                result = self.animals_collection.update_one(
                    {"_id": ObjectId(animal_id)},
                    {"$set": update_fields}
                )
                if result:
                    self.logger.info(f"id={request_id} Animal updated successfully")
                    return ResponseDTO(None, "Animal updated successfully", http.HTTPStatus.OK)
                else:
                    self.logger.error(f"id={request_id} Error on update animal")
                    return ResponseDTO(None, "Error on update animal", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"id={request_id} Error updating animal: {e}")
            return ResponseDTO(None, "Error on update animal", http.HTTPStatus.BAD_REQUEST)

    def delete_animal(self, animal_id: str, request_id: str = "") -> bool:
        try:
            with self.db.session.start_transaction():
                # TODO: Deleção lógica
                result = self.animals_collection.delete_one({"_id": ObjectId(animal_id)})
                return True if result else False
        except Exception as e:
            self.logger.error(f"id={request_id} Error deleting animal: {e}")
            return False

    def get_animal_by_id(self, animal_id: str, ong_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            response = self.ong_service.get_ong_by_id(ong_id, request_id)
            if response.status != http.HTTPStatus.OK:
                return response
            
            result = self.animals_collection.find_one({"_id": ObjectId(animal_id)})

            if not result:
                self.logger.info(f"id={request_id} Animal not found")
                return ResponseDTO(None, "Animal not found", http.HTTPStatus.NOT_FOUND)

            response = self.ong_service.get_ong_animals(ong_id, request_id)
            if response.status != http.HTTPStatus.OK:
                return response
            
            # TODO: Melhorar isso usando dicionario ao inves de lista de animais
            ong_animals = response.data
            has_animal = False
            for animal in ong_animals:
                if animal["id"] == animal_id:
                    has_animal = True
                    break
            if not has_animal:
                self.logger.error(f"id={request_id} Animals doesn't belong to ong")
                return ResponseDTO(None, "Animals doesn't belong to ong", http.HTTPStatus.BAD_REQUEST)                
            self.logger.info(f"id={request_id} Animal retrieved successfully")
            return ResponseDTO(AnimalModel.helper(result), "Animal retrieved successfully", http.HTTPStatus.OK)
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting animal: {e}")
            return ResponseDTO(None, "Error on get animal", http.HTTPStatus.BAD_REQUEST)
    
    def insert_form(self, animal_id: str, form_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                result = self.animals_collection.update_one(
                    {"_id": ObjectId(animal_id)},
                    {"$push": {"forms": form_id}}
                )
                if result:
                    self.logger.info(f"id={request_id} Form inserted")
                    return ResponseDTO(result, "Form inserted", http.HTTPStatus.OK)
                else:
                    self.logger.error(f"id={request_id} Error inserting form in animal")
                    return ResponseDTO(None, "Error inserting form in animal", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"id={request_id} Error updating animal forms: {e}")          
            return ResponseDTO(None, "Error updating animal forms", http.HTTPStatus.BAD_REQUEST)

    def get_forms_from_animal(self, animal_id: str, ong_id: str, request_id = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            response = self.get_animal_by_id(animal_id, ong_id, request_id)
            if response.status != http.HTTPStatus.OK:
                return response

            result = list(self.animals_collection.aggregate([
                {
                    "$match": {"_id": ObjectId(animal_id)}
                },
                {
                    "$lookup": {
                        "from": "forms",
                        "localField": "forms",
                        "foreignField": "_id",
                        "as": "forms"
                    }
                },
                {
                    "$unwind": "$forms"
                },
                {
                    "$sort": {"forms.created_at": -1, "forms.title": 1}
                },
                {
                    "$project": {
                        "forms": 1
                    }
                }
            ]))
            self.logger.debug(result)
            if result:
                # TODO: Criar um DTO Especifico para esse caso e outros
                forms = [{"id": str(form['forms']["_id"]), "title": form['forms']["title"]} for form in result]
                self.logger.info(f"id={request_id} Form retrieved successfully")
                return ResponseDTO(forms, "Form retrieved successfully", http.HTTPStatus.OK)
            self.logger.info(f"id={request_id} Animal has no forms")
            return ResponseDTO([], "Animal has no forms", http.HTTPStatus.OK)
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting forms from animal: {e}")
            return ResponseDTO(None, "Error getting forms from animal", http.HTTPStatus.BAD_REQUEST)