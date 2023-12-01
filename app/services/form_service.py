import http
import logging
from bson import ObjectId
from app.domain.database.db import Database
from app.domain.models.form import FormModel
from app.domain.models.dto.response import ResponseDTO
from app.services.ong_service import OngService
from app.services.animal_service import AnimalService
from app.domain.models.answerSheet import AnswerSheetModel

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
                if response.status != http.HTTPStatus.OK or not response.data: #baseado no reponse.data
                    #TODO; logging nao tem animal na ong
                    return ResponseDTO(None, "Ong has no animals", http.HTTPStatus.BAD_REQUEST)
                animals = response.data
                animal_exist = False
                for animal in animals:
                    if str(animal.get("id")) == animal_id:
                        animal_exist = True
                        break
                if not animal_exist:
                    return ResponseDTO(None, "Animal doesn't belongs to ONG. Aborting.", http.HTTPStatus.BAD_REQUEST)
                form.animal_id = animal_id
                result = self.form_collection.insert_one(form.model_dump())
                if result:
                    response = self.animal_service.insert_form(animal_id, result.inserted_id)
                    # TODO: tratar rollback
                    if response.status != http.HTTPStatus.OK:
                        return response
                    #new_form = self.form_collection.find_one(result.inserted_id)
                    return ResponseDTO({"id": result.inserted_id},"Form created successfully", http.HTTPStatus.CREATED)
                else:
                    return ResponseDTO(None, "Couldn't Create Form. Aborting.", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error creating Forms: {e}")
            return ResponseDTO(None, "Error Creating Form: " + str(e), http.HTTPStatus.BAD_REQUEST)
    
    def get_form_by_id(self, ong_id: str,  animal_id:str, form_id: str, request_id: str = "") -> ResponseDTO:
        self.logger.info(f"id = {request_id} starting get form by id")
        try:
            response = self.ong_service.get_ong_animals(ong_id)
            if response.status != http.HTTPStatus.OK:
                return response
            animals = response.data
            if not animals:
                 return ResponseDTO(None, "There is no animals in ONG.", http.HTTPStatus.BAD_REQUEST)
            animal_exist = False
            animal_object = None
            form_exist = False
            for animal in animals:
                if str(animal.get("id")) == animal_id:
                    animal_exist = True
                    animal_object = animal
                    break
            if not animal_exist:
                return ResponseDTO(None, "Animal doesn't belongs to ONG.", http.HTTPStatus.BAD_REQUEST)
            
            for form in animal_object.get("forms"):
                if form == form_id:
                    form_exist = True
                    break
                
            if not form_exist:
                return ResponseDTO(None, "This form doesn't belong to this animal", http.HTTPStatus.BAD_REQUEST)
            return self.get_form(form_id, request_id)
            
        except Exception as e:
            message = f"Error getting Form: {e}"
            print(message)
            return ResponseDTO(None, message, http.HTTPStatus.BAD_REQUEST)
    
    def get_form (self, form_id: str, request_id: str = "")-> ResponseDTO:
        self.logger.info(f"id = {request_id} starting get form")
        try:
            result = self.form_collection.find_one({"_id": ObjectId(form_id)})
            if result:
                self.logger.info(f"id = {request_id} Form gottern successfully")
                return ResponseDTO(FormModel.helper(result),"Form gotten successfully", http.HTTPStatus.OK)
            self.logger.error(f"id = {request_id} error getting form")
            return ResponseDTO(None, "Couldn't find Form. Aborting.", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            message = f"Error getting Form: {e}"
            print(message)
            self.logger.error(f"id = {request_id} {message}")
            return ResponseDTO(None, message, http.HTTPStatus.BAD_REQUEST)  
        
    def get_questions(self, ong_id: str,  animal_id:str, form_id: str, answers: bool = False) -> ResponseDTO:
        response = self.get_form_by_id(ong_id, animal_id, form_id)
        if response.status != http.HTTPStatus.OK:
            return response
        questions = response.data.get("questions")
        for q in questions:
            new_choice = []
            for c in q.get('choices'):
                new_choice.append(c[0])
            q['choices'] = new_choice
            print(q)
        del response.data['animal_id']
        del response.data['answer_sheets']
        return response
    
    def get_answer_sheets(self, form_id: str, request_id:str = "") -> ResponseDTO:
        try:
            result = list(self.form_collection.aggregate([
                {
                    "$match": {"_id": ObjectId(form_id)}
                },
                {
                    "$lookup": {
                        "from": "answer_sheets",
                        "localField": "answer_sheets",
                        "foreignField": "_id",
                        "as": "answer_sheets"
                    }
                },
                {
                    "$sort": {"answer_sheets.created_at": -1, "answer_sheets.name": 1}
                },
                {
                    "$project": {
                        "answer_sheets": 1
                    }
                }
            ]))
            if result:
                answers = [AnswerSheetModel.helper(answer) for answer in result[0]["answer_sheets"]]
                self.logger.info(f"id={request_id} form answers retrieved successfully")
                print(result, answers)
                return ResponseDTO(answers, "form answers retrieved successfully", http.HTTPStatus.OK)
            self.logger.info(f"id={request_id} form has no answers")
            return ResponseDTO([], "form has no answers", http.HTTPStatus.OK)
        except Exception as e:
            self.logger.error(f"id={request_id} Error getting form answers: {e}")
            return ResponseDTO(None, "Error on get form answers", http.HTTPStatus.BAD_REQUEST)

    def get_forms_from_animal(self, animal_id:str, ong_id: str, request_id:str = ""):
        self.logger.info(f"id={request_id} Start service")
        try:
            response = self.animal_service.get_animal(animal_id, ong_id, request_id)
            if not response.data:
                return response
            self.logger.info(f"id={request_id} Getting query")
            pipeline = [
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
                        "$sort": {"forms.created_at": -1, "forms.name": 1}
                    },
                    {
                        "$project": {
                            "forms":{
                                "_id":1,
                                "title":1
                            }
                        }
                    }
            ]
            result = list(self.animal_service.animals_collection.aggregate(pipeline))
            if result:
                forms = [FormModel.helper(form) for form in result[0]["forms"]]
                '''for form in forms:
                    del form["animal_id"]
                    del form["questions"]
                    del form["answer_sheets"]'''
                self.logger.info(f"id={request_id} Forms retrived successfully")
                return ResponseDTO(forms, "Forms retrived sucessfully", http.HTTPStatus.OK)
            self.logger.info(f"id={request_id} Animal has no forms")
            
        except Exception as e:
            self.logger.error(f"if={request_id} Error getting form {e}")
            return ResponseDTO(None, "Error getting forms from animal", http.HTTPStatus.BAD_REQUEST)
        
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
    