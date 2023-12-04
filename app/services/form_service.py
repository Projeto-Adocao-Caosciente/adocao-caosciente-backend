from datetime import datetime
import http
import logging
from bson import ObjectId
from app.domain.database.db import Database
from app.domain.models.form import FormModel
from app.domain.models.dto.response import ResponseDTO
from app.services.ong_service import OngService
from app.services.animal_service import AnimalService

class FormService:
    def __init__(self,ong_service: OngService, animal_service: AnimalService):
        self.db = Database()
        self.ong_service = ong_service
        self.animal_service = animal_service
        self.form_collection = self.db.get_database().get_collection("forms")
        self.logger = logging.getLogger(__name__)
        
    def create_form(self, ong_id:str, animal_id:str, form: FormModel, request_id:str = "") -> ResponseDTO:
        self.logger.info(f"id = {request_id} starting create form")
        try:
            with self.db.session.start_transaction():
                response = self.ong_service.get_ong_animals(ong_id)
                if response.status != http.HTTPStatus.OK: 
                    return ResponseDTO(None, "Ong has no animals", http.HTTPStatus.BAD_REQUEST)
                
                animals = response.data
                if not animals:
                    self.logger.error(f"id = {request_id} There is no animal in Ong")
                    return ResponseDTO(None, "The current ONG has no animals", http.HTTPStatus.BAD_REQUEST)
                
                has_animal = False
                for animal in animals:
                    if str(animal.get("id")) == animal_id:
                        self.logger.info(f"id = {request_id} Found Animal")
                        has_animal = True
                        break

                if not has_animal:
                    self.logger.info(f"id = {request_id} Animal not Found")
                    return ResponseDTO(None, "Animal doesn't belongs to ONG.", http.HTTPStatus.BAD_REQUEST)
                
                form.animal_id = animal_id
                current_time = datetime.now().isoformat()
                form.created_at = current_time
                form.updated_at = current_time
                result = self.form_collection.insert_one(form.model_dump())
                if result:
                    response = self.animal_service.insert_form(animal_id, result.inserted_id)
                    # TODO: tratar rollback
                    if response.status != http.HTTPStatus.OK:
                        return response
                    #new_form = self.form_collection.find_one(result.inserted_id)
                    self.logger.info(f"id= {request_id} Form Created Sucessfully")
                    return ResponseDTO({"id": str(result.inserted_id)},"Form created successfully", http.HTTPStatus.CREATED)
                else:
                    self.logger.error(f"id= {request_id} Couldn't Create Form")
                    return ResponseDTO(None, "Couldn't Create Form", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"id= {request_id} Error creating form {e}")
            return ResponseDTO(None, "Error Creating Form", http.HTTPStatus.BAD_REQUEST)
    
    def get_form_by_id(self, ong_id: str, form_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id = {request_id} starting get form by id")
        response = self.get_form_by_ong(form_id, ong_id, request_id)
        if response.status != http.HTTPStatus.OK:
            return response

        self.logger.info(f"id = {request_id} Form retrieved successfully")
        return ResponseDTO(response.data, "Form retrieved successfully", http.HTTPStatus.OK)
    
    def get_questions(self, form_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id = {request_id} starting get form questions")
        try:
            with self.db.session.start_transaction():
                result = self.form_collection.find_one({"_id": ObjectId(form_id)})
                if not result:
                    self.logger.error(f"id = {request_id} Form doesn't exists")
                    return ResponseDTO(None, "Form doesn't exists", http.HTTPStatus.NOT_FOUND)
                form_questions = result["questions"]
                # delete is_correct field
                for question in form_questions:
                    for choice in question["choices"]:
                        del choice["is_correct"]

                self.logger.info(f"id = {request_id} Form questions retrieved successfully")
                return ResponseDTO(form_questions, "Form questions retrieved successfully", http.HTTPStatus.OK)
            
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting form questions: {e}")          
            return ResponseDTO(None, "Error getting form questions", http.HTTPStatus.NOT_FOUND)

    def get_answer_sheets(self, form_id: str, ong_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id = {request_id} starting get form answer sheets")
        response = self.get_form_by_ong(form_id, ong_id, request_id)
        if response.status != http.HTTPStatus.OK:
            return response
        
        form_answer_sheets = response.data["answer_sheets"]

        self.logger.info(f"id = {request_id} Form retrieved successfully")
        return ResponseDTO(form_answer_sheets, "Form retrieved successfully", http.HTTPStatus.OK)
        
    def insert_answer(self, form_id: str, answer_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                result = self.form_collection.update_one(
                    {"_id": ObjectId(form_id)},
                    {"$push": {"answer_sheets": answer_id}}
                )
                if result:
                    self.logger.info(f"id={request_id} answer inserted in form")
                    return ResponseDTO(result, "answer inserted in form", http.HTTPStatus.OK)
                else:
                    self.logger.error(f"id={request_id} Could not insert answer")
                    return ResponseDTO(None, "Could not insert answer", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"id={request_id} Error update form answer: {e}")          
            return ResponseDTO(None, "Error update form anwer", http.HTTPStatus.BAD_REQUEST)
    
    def get_form_by_ong(self, form_id: str, ong_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id={request_id} starting service")
        try:
            result = list(self.ong_service.ongs_collection.aggregate([
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
                    "$lookup": {
                        "from": "forms",
                        "localField": "animals.forms",
                        "foreignField": "_id",
                        "as": "animals.forms"
                    }
                },
                {
                    "$unwind": "$animals.forms"
                },
                {
                    "$match": {"animals.forms._id": ObjectId(form_id)}
                },
                {
                    "$project": {
                        "forms": {
                            "id": { "$toString": "$_id" },
                            "title": "$animals.forms.title",
                            "questions": "$animals.forms.questions",
                            "answer_sheets": "$animals.forms.answer_sheets",
                        }
                    },
                }
            ]))
            if not result:
                self.logger.error(f"id={request_id} There is not fully relationship between ong, animal, form")
                return ResponseDTO(None, "There is not fully relationship between ong, animal, form", http.HTTPStatus.BAD_REQUEST)

            if result:
                self.logger.info(f"id={request_id} Form retrieved successfully")
                return ResponseDTO(result[0]["forms"], "Form retrieved successfully", http.HTTPStatus.OK)
            
            self.logger.info(f"id={request_id} Error getting form.")
            return ResponseDTO(None, "Error getting form", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting form: {e}")
            return ResponseDTO(None, "Error getting form", http.HTTPStatus.BAD_REQUEST)