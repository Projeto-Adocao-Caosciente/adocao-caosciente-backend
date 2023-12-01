from pydantic import BaseModel, Field

class AnswerSheetModel(BaseModel):
    adopter_id: str
    form_id: str
    score: int
    answers: list[int] = []
    
    class Config:
        schema_extra = {
            "adopter_id": "653efb24188b172ef77d8acc",
            "form_id": "653efee7eb19804a4a56fc86",
            "score": 7,
            "answers": [1,2,4,2,3,2]
        }

    def __dict__(self):
        return {
            'form_id': self.form_id,
            'score': self.score,
            'answers': self.answers,
        }
        
    @staticmethod
    def answer_sheet_helper(answer_sheet):
        return {
            "id": str(answer_sheet["_id"]),
            "adopter_id": str(answer_sheet["adopter_id"]),
            "form_id": str(answer_sheet["form_id"]),
            "score": answer_sheet["score"],
            "answers": answer_sheet["answers"]
        }
        