import http
import logging
from bson import ObjectId
from app.domain.database.db import Database
from app.domain.models.form import FormModel
from app.domain.models.answerSheet import AnswerSheetModel
from app.domain.models.dto.response import ResponseDTO
from app.services.form_service import FormService
from app.services.adopter_service import AdopterService


class AnswerSheetService:
    # TODO: Fix when rebasing with adopter CR
    def __init__(self, form_service: FormService, adopter_service: AdopterService):
        self.db = Database()
        self.form_service = form_service
        self.adopter_service = adopter_service
        self.answer_sheet_collection = self.db.get_database().get_collection("answer_sheets")
        self.logger = logging.getLogger(__name__)

    def create_answer_sheet(self, adopter_id: str, form_id: str,  answerSheet: AnswerSheetModel, request_id: str = ""):
        self.logger.info(f"id={request_id} Start service create answer Sheet")
        try:
            with self.db.session.start_transaction():
                response = self.db.get_database().get_collection("adopter").find_one({"_id": ObjectId(adopter_id)})
                if not response:
                    self.logger.error(f"id={request_id} User is not an adopter")
                    return ResponseDTO(None, "User is not an adopter", http.HTTPStatus.BAD_REQUEST)
                answerSheet.adopter_id = adopter_id
                answerSheet.form_id = form_id
                result_form = self.form_service.form_collection.find_one({"_id": ObjectId(form_id)})
                if not result_form:
                    self.logger.error(f"id={request_id} Form not found")
                    return ResponseDTO(None, "Form not Found", http.HTTPStatus.BAD_REQUEST)
                if len(result_form.get("questions")) != len(answerSheet.model_dump().get("answers")):
                    self.logger.error(f"id={request_id} Invalid Answers, Wrong number of answers")
                    return ResponseDTO(None, "Invalid Answers", http.HTTPStatus.BAD_REQUEST)
                
                self.logger.info(f"id={request_id} checking if choices are valid")
                for q, c in zip(result_form.get("questions"), answerSheet.model_dump().get("answers")):
                    if len(q.get("choices")) <= c or c < 0:
                        self.logger.error(f"id={request_id} {c} is an invalid choice for the question")
                        return ResponseDTO(None, f"{c} is an invalid choice for the question {q.get("question")}", http.HTTPStatus.BAD_REQUEST)
                
                self.logger.info(f"id={request_id} Inserting answers in collection")
                result = self.answer_sheet_collection.insert_one(answerSheet.model_dump())
                if result:
                    self.logger.info(f"id={request_id} Answer Sheet Created Successfully")
                    adopter_response = self.adopter_service.insert_answer(adopter_id, result.inserted_id)
                    if adopter_response.data is None:
                        self.logger.error(f"id={request_id} Error on Create answer sheet, unable to insert answersheet in adopter")
                        self.answer_sheet_collection.delete_one(ObjectId(result.inserted_id))
                        return ResponseDTO(None, f"Error on Create answer sheet, unable to insert answersheet in adopter", http.HTTPStatus.BAD_GATEWAY )
                    form_response = self.form_service.insert_answer(form_id, result.inserted_id)
                    if form_response.data is None:
                        # TODO: remove only the element inserted in line 49
                        self.answer_sheet_collection.delete_one({"_id": ObjectId(result.inserted_id)})
                        self.logger.error(f"id={request_id} Error on Create answer sheet, unable to insert answersheet in form")
                        return ResponseDTO(None, f"Error on Create answer sheet, unable to insert answersheet in form", http.HTTPStatus.BAD_GATEWAY )
                    self.logger.info(f"id={request_id} Answer Sheet Inserted succesfully")
                    return ResponseDTO({"id":str(result.inserted_id)}, "Answer Sheet created successfully", http.HTTPStatus.CREATED)
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
            result = self.answer_sheet_collection.find_one({"_id": ObjectId(answerSheet_id)})
            if result:
                self.logger.info(f"id={request_id} success getting answer sheet")
                return ResponseDTO(FormModel.helper(result),"Answer Sheet gotten successfully", http.HTTPStatus.OK)
            self.logger.info(f"id= {request_id} Couldn't find Answer Sheet")
            return ResponseDTO(None, "Couldn't find Answer Sheet", http.HTTPStatus.BAD_REQUEST)
        except Exception as e:
            msg = f"Error getting Answer Sheet: {e}"
            self.logger.error(f"id={request_id} {msg}")
            return ResponseDTO(None, msg, http.HTTPStatus.BAD_REQUEST)


    