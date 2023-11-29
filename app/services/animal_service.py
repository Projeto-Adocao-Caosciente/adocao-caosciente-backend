from datetime import datetime
import http
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

    def create_animal(self, animal: AnimalModel, ong_id: str) -> ResponseDTO:
        try:
            with self.db.session.start_transaction():
                current_time = datetime.now().isoformat()
                animal.created_at = current_time
                animal.updated_at = current_time

                response = self.ong_service.get_ong_by_id(ong_id)
                if response.status != http.HTTPStatus.OK:
                    return response
                
                ong_id = response.data["id"]

                result = self.animals_collection.insert_one(animal.model_dump())
                if not result:
                    return ResponseDTO(None, "Error on create animal", http.HTTPStatus.BAD_REQUEST)
                
                response = self.ong_service.update_ong_animals(ong_id, result.inserted_id)
                if response.status != http.HTTPStatus.OK:
                    return response
                
                return ResponseDTO({"id": str(result.inserted_id)}, "Animal created successfully", http.HTTPStatus.CREATED)
        except Exception as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error creating animal: {e}")
            return ResponseDTO(None, "Error on create animal", http.HTTPStatus.BAD_REQUEST)

    def update_animal(self, animal: AnimalModel, animal_id: str, ong_id: str) -> ResponseDTO:
        try:
            with self.db.session.start_transaction():
                response = self.get_animal(animal_id, ong_id)
                if response.status != http.HTTPStatus.OK:
                    return response
                
                old_animal = response.data

                update_fields = { field : value for field, value in animal.model_dump().items() if value != old_animal[field] and value is not None }
                if len(update_fields) == 0:
                    return ResponseDTO(None, "Animal not modified", http.HTTPStatus.OK)

                animal.updated_at = datetime.now().isoformat()
                result = self.animals_collection.update_one(
                    {"_id": ObjectId(animal_id)},
                    {"$set": update_fields}
                )
                if result:
                    return ResponseDTO(None, "Animal updated successfully", http.HTTPStatus.OK)
                else:
                    return ResponseDTO(None, "Error on update animal", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error updating animal: {e}")
            return ResponseDTO(None, "Error on update animal", http.HTTPStatus.BAD_REQUEST)

    def delete_animal(self, animal_id: str) -> bool:
        try:
            with self.db.session.start_transaction():
                # TODO: Deleção lógica
                result = self.animals_collection.delete_one({"_id": ObjectId(animal_id)})
                return True if result else False
        except Exception as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error deleting animal: {e}")
            return False

    def get_animal(self, animal_id: str, ong_id: str) -> ResponseDTO:
        try:
            response = self.ong_service.get_ong_by_id(ong_id)
            if response.status != http.HTTPStatus.OK:
                return response
            
            result = self.animals_collection.find_one({"_id": ObjectId(animal_id)})

            if not result:
                return ResponseDTO(None, "Animal not found", http.HTTPStatus.NOT_FOUND)

            response = self.ong_service.get_ong_animals(ong_id)
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
                return ResponseDTO(None, "Animals doesn't belong to ong", http.HTTPStatus.UNAUTHORIZED)                
            
            return ResponseDTO(AnimalModel.animal_helper(result), "Animal retrieved successfully", http.HTTPStatus.OK)
        except Exception as e:
            # TODO: Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error getting animal: {e}")
            return None
    
    def insert_form(self, animal_id: str, form_id: str) -> ResponseDTO:
        try:
            with self.db.session.start_transaction():
                result = self.animals_collection.update_one(
                    {"_id": ObjectId(animal_id)},
                    {"$push": {"forms": form_id}}
                )
                if result:
                    return ResponseDTO(result, "Form inserted", http.HTTPStatus.OK)
                else:
                    return ResponseDTO(None, "Could not insert form", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error update animal forms: {e}")
            return ResponseDTO(None, "Error update animal forms", http.HTTPStatus.BAD_REQUEST)

