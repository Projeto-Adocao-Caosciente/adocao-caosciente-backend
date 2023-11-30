import http
from bson import ObjectId
from app.domain.database.db import Database
from app.domain.models.form import FormModel
from app.domain.models.answerSheet import AnswerSheetModel
from app.domain.models.dto.response import ResponseDTO
from app.services.ong_service import OngService
from app.services.animal_service import AnimalService
from app.services.form_service import FormService
from app.services.adopter_service import AdopterService


class AnswerSheetService:
    # TODO: Fix when rebasing with adopter CR
    def __init__(self,ong_service: OngService, animal_service: AnimalService, form_service: FormService, adopter_service: AdopterService):
        self.db = Database()
        self.ong_service = ong_service
        self.animal_service = animal_service
        self.form_service = form_service
        self.adopter_service = adopter_service
        self.answer_sheet_collection = self.db.get_database().get_collection("answer_sheets")
    
    def create_answer_sheet(self, user_id: str, form_id: str,  answerSheet: AnswerSheetModel):
        try:
            with self.db.session.start_transaction():
                answerSheet.adopter_id = user_id
                answerSheet.form_id = form_id
                result = self.answer_sheet_collection.insert_one(answerSheet.dict())
                if result:
                    self.adopter_service.insert_answer(user_id, result.inserted_id)
                    return ResponseDTO(AnswerSheetModel.answer_sheet_helper(result),"Answer Sheet created successfully", http.HTTPStatus.OK)
                else:
                    return ResponseDTO(None, "Couldn't Create Answer Sheet. Aborting.", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            print(f"Error creating Answer Sheet: {e}")
            return ResponseDTO(None, "Error Creating Answer Sheet: " + e, http.HTTPStatus.BAD_REQUEST)
        
    def get_answer_sheet(self, answerSheet_id: str, user_id: str):
        try:
            user =  self.adopter_service.get_adopter_by_id(user_id)
            if answerSheet_id not in user.get('answer_sheets'):
                return ResponseDTO(None, "Answer Sheet doesn't belong to user. Aborting.", http.HTTPStatus.BAD_REQUEST)
            result = self.answerSheets_collection.find_one({"_id": ObjectId(answerSheet_id)})
            if result:
                return ResponseDTO(FormModel.form_helper(result),"Answer Sheet gotten successfully", http.HTTPStatus.OK)
            return ResponseDTO(None, "Couldn't find Answer Sheet. Aborting.", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            print(f"Error getting Answer Sheet: {e}")
            return ResponseDTO(None, "Erro Getting Answer Sheet:"+e, http.HTTPStatus.BAD_REQUEST)
    

    