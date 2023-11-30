import http
import logging
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
        self.logger = logging.getLogger(__name__)

    def create_answer_sheet(self, user_id: str, form_id: str,  answerSheet: AnswerSheetModel, request_id: str = ""):
        self.logger.info(f"id={request_id} Start service")
        try:
            with self.db.session.start_transaction():
                answerSheet.adopter_id = user_id
                answerSheet.form_id = form_id
                result = self.answer_sheet_collection.insert_one(answerSheet.dict())
                if result:
                    self.logger.info(f"id={request_id} Answer Sheet Created Successfully")
                    self.adopter_service.insert_answer(user_id, result.inserted_id)
                    return ResponseDTO(AnswerSheetModel.answer_sheet_helper(result),"Answer Sheet created successfully", http.HTTPStatus.CREATED)
                else:
                    self.logger.error(f"id={request_id} Error on Create answer sheet")
                    return ResponseDTO(None, "Error on Create Answer Sheet.", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"id={request_id} Error creating answer Sheet: {e}")
            msg= f"Error creating Answer Sheet: {e}"
            return ResponseDTO(None, msg, http.HTTPStatus.BAD_REQUEST)
        
    def get_answer_sheet(self, answerSheet_id: str, user_id: str, request_id:str = ""):
        self.logger.info(f"id={request_id} Start service")
        try:
            user =  self.adopter_service.get_adopter_by_id(user_id)
            if answerSheet_id not in user.get('answer_sheets'):
                self.logger.error(f"id={request_id} Error getting answer: answersheet doesn't belong to user")
                return ResponseDTO(None, "Answer Sheet doesn't belong to user", http.HTTPStatus.BAD_REQUEST)
            result = self.answerSheets_collection.find_one({"_id": ObjectId(answerSheet_id)})
            if result:
                self.logger.info(f"id={request_id} success getting answer sheet")
                return ResponseDTO(FormModel.form_helper(result),"Answer Sheet gotten successfully", http.HTTPStatus.OK)
            self.logger.info(f"id= {request_id} Couldn't find Answer Sheet")
            return ResponseDTO(None, "Couldn't find Answer Sheet", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            msg = f"Error getting Answer Sheet: {e}"
            self.logger.error(f"id={request_id} {msg}")
            return ResponseDTO(None, msg, http.HTTPStatus.BAD_REQUEST)
    

    