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
        
    def create_form(self, ong_id:str, animal_id:str, form: FormModel) -> ResponseDTO:
        try:
            with self.db.session.start_transaction():
                response = self.ong_service.get_ong_animals(ong_id)
                if response.status != http.HTTPStatus.OK:
                    return response
                animals = response.data
                has_animal = False
                for animal in animals:
                    if str(animal.get("id")) == animal_id:
                        has_animal = True
                        break
                if not has_animal:
                    return ResponseDTO(None, "Animal doesn't belongs to ONG. Aborting.", http.HTTPStatus.BAD_REQUEST)
                form.animal_id = animal_id
                result = self.form_collection.insert_one(form.model_dump())
                if result:
                    response = self.animal_service.insert_form(animal_id, result.inserted_id)
                    if response.status != http.HTTPStatus.OK :
                        return response
                    new_form = self.form_collection.find_one(result.inserted_id)
                    return ResponseDTO(FormModel.form_helper(new_form),"Form created successfully", http.HTTPStatus.CREATED)
                else:
                    return ResponseDTO(None, "Couldn't Create Form. Aborting.", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            # TODO:Utilizar a biblioteca logging para criar uma documentação clara do que esta rolando na api. Nota: Isso facilita o debug e rastreabilidade tmb
            print(f"Error creating Forms: {e}")
            return ResponseDTO(None, "Error Creating Form: " + str(e), http.HTTPStatus.BAD_REQUEST)
    
    def get_form_by_id(self, ong_id: str,  animal_id:str, form_id: str) -> ResponseDTO:
        try:
            response = self.ong_service.get_ong_animals(ong_id)
            if response.status != http.HTTPStatus.OK:
                return response
            animals = response.data

            has_animal = False
            animal_object = None
            has_form = False
            for animal in animals:
                if str(animal.get("id")) == animal_id:
                    has_animal = True
                    animal_object = animal
                    break
            if not has_animal:
                return ResponseDTO(None, "Animal doesn't belongs to ONG.", http.HTTPStatus.BAD_REQUEST)
            
            for f in animal_object.get("forms"):
                if f == form_id:
                    has_form = True
            
            if not has_form:
                return ResponseDTO(None, "This form doesn't belong to this animal", http.HTTPStatus.BAD_REQUEST)
            result = self.form_collection.find_one({"_id": ObjectId(form_id)})
            if result:
                return ResponseDTO(FormModel.form_helper(result),"Form gotten successfully", http.HTTPStatus.OK)
            return ResponseDTO(None, "Couldn't find Form. Aborting.", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            message = f"Error getting Form: {e}"
            print(message)
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
    
    
    def get_answer_sheets(self, formID) -> ResponseDTO:
        #TODO: Retorna uma lista dos IDs das folhas de respostas dos participantes
        return
