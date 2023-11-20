import http
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
        
    def create_form(self, ong_id:str, animal_id:str, form: FormModel):
        try:
            with self.db.session.start_transaction():
                animals = self.ong_service.get_ong_animals(ong_id)
                has_animal = False
                for animal in animals:
                    if str(animal.get("id")) == animal_id:
                        has_animal = True
                        break
                if not has_animal:
                    return ResponseDTO(http.HTTPStatus.BAD_REQUEST, "Animal doesn't belongs to ONG. Aborting.", None)
                form.animal_id = animal_id
                result = self.form_collection.insert_one(form.dict())
                if result:
                    self.animal_service.insert_form(animal_id, result.inserted_id)
                    new_form = self.form_collection.find_one(result.inserted_id)
                    return ResponseDTO(http.HTTPStatus.CREATED,"Form created successfully", FormModel.form_helper(new_form))
                else:
                    return ResponseDTO(http.HTTPStatus.BAD_REQUEST, "Couldn't Create Form. Aborting.", None)
        except Exception as e:
            print(f"Error creating Forms: {e}")
            return ResponseDTO(http.HTTPStatus.BAD_REQUEST, "Error Creating Form: " + str(e), None)
    
    def get_form_by_id(self, ong_id: str,  animal_id:str, form_id: str):
        try:
            animals = self.ong_service.get_ong_animals(ong_id)
            has_animal = False
            animal_object = None
            has_form = False
            for animal in animals:
                if str(animal.get("id")) == animal_id:
                    has_animal = True
                    animal_object = animal
                    break
            if not has_animal:
                return ResponseDTO(http.HTTPStatus.BAD_REQUEST, "Animal doesn't belongs to ONG. Aborting.", None)
            
            for f in animal_object.get("forms"):
                if f == form_id:
                    has_form = True
            
            if not has_form:
                return ResponseDTO(http.HTTPStatus.BAD_REQUEST, "This form doesn't belong to this animal", None)
            result = self.form_collection.find_one({"_id": ObjectId(form_id)})
            if result:
                return ResponseDTO(200,"Form gotten successfully", FormModel.form_helper(result))
            return ResponseDTO(400, "Couldn't find Form. Aborting.", None)
        except Exception as e:
            message = f"Error getting Form: {e}"
            print(message)
            return ResponseDTO(400, message, None)
        
        
    def get_questions(self, ong_id: str,  animal_id:str, form_id: str, answers: bool = False) -> ResponseDTO:
        result = self.get_form_by_id(ong_id, animal_id, form_id)
        if result.status != 200:
            return result
        questions = result.data.get("questions")
        for q in questions:
            new_choice = []
            for c in q.get('choices'):
                new_choice.append(c[0])
            q['choices'] = new_choice
            print(q)
        del result.data['animal_id']
        del result.data['answer_sheets']
        return result
    
    
    def get_answer_sheets(self, formID) -> ResponseDTO:
        #TODO: Retorna uma lista dos IDs das folhas de respostas dos participantes
        return
