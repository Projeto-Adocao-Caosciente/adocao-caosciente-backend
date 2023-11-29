from datetime import datetime
from bson import ObjectId
import http
from pymongo.errors import DuplicateKeyError

from app.domain.database.db import Database
from app.domain.models.adopter import AdopterModel
from app.domain.models.animal import AnimalModel
from app.domain.models.dto.response import ResponseDTO


class AdopterService:
    def __init__(self):
        self.db = Database()
        self.adopter_collection = self.db.get_database().get_collection("adopter")

    def create_adopter(self, adopter: AdopterModel) -> ResponseDTO:
        try:
            with self.db.session.start_transaction():
                # FIXME: Encriptar senha de alguma forma, aqui dá erro -> 'OngModel' object has no attribute 'password'
                # salt = bcrypt.gensalt()  # definir rounds torna a operação mais lenta
                # ong.password = bcrypt.hashpw(
                current_time = datetime.now().isoformat()
                adopter.created_at = current_time
                adopter.updated_at = current_time
                result = self.adopter_collection.insert_one(adopter.model_dump())
                if result:
                    return ResponseDTO({"id": str(result.inserted_id)}, "Adopter created successfully", http.HTTPStatus.CREATED)
                else:
                    return ResponseDTO(None, "Error on create adopter", http.HTTPStatus.BAD_REQUEST)
        except DuplicateKeyError as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error creating adopter: {e}")
            duplicated_field = str(e).split("index: ")[1].split("_")[0]
            return ResponseDTO(None, duplicated_field + " already in use", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            print(f"Erro creating adopter: {e}")
            return ResponseDTO(None, "Error on create adopter", http.HTTPStatus.BAD_REQUEST)

    def get_adopter_by_id(self, adopter_id: str) -> ResponseDTO:
        print(adopter_id)
        try:
            result = self.adopter_collection.find_one({"_id": ObjectId(adopter_id)})
            if result:
                return ResponseDTO(AdopterModel.adopter_helper(result), "Adopter retrieved successfully", http.HTTPStatus.OK)
            return ResponseDTO(None, "Adopter not found", http.HTTPStatus.NOT_FOUND)
        except Exception as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error getting adopter: {e}")
            return ResponseDTO(None, "Error getting adopter", http.HTTPStatus.BAD_REQUEST)
        
    def get_adopter_by_cpf(self, cpf: str):
        try:
            result = self.adopter_collection.find_one({"cpf": cpf})
            if result:
                return result
            return None
        except Exception as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error getting adopter by cpf: {e}")
            return None
        
    def get_adopter_animals(self, adopter_id: str) -> ResponseDTO:
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
                animals = [AnimalModel.animal_helper(animal) for animal in result[0]["animals"]]
                return ResponseDTO(animals, "Adopter animals retrieved successfully", http.HTTPStatus.OK)
            return ResponseDTO([], "Adopter has no animals", http.HTTPStatus.OK)
        except Exception as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error getting adopter animals: {e}")
            return ResponseDTO(None, "Error on get adopter animals", http.HTTPStatus.BAD_REQUEST)