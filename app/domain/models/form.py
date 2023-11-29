from typing import List
from pydantic import BaseModel
class FormModel(BaseModel):
    title: str = None
    animal_id: str = None
    questions: List[dict] = []
    answer_sheets: List[str] = []
    
    class Config:
        json_schema_extra = {
            "title": "Questionario",
            "animal_id": "653efb24188b172ef77d8acc",
            "questions": [
                {
                    "question": "Essa é uma pergunta?",
                    "choices": [("Sim", "True"), ("Não", "False"), ("É Sim", "True")]
                },
                {
                    "question": "Voce Mora em:",
                    "choices": [("Casa", "True"), ("Apartamento", "True"), ("Van", "False")]
                }
            ]
        }

    def __dict__(self):
        return {
            'title': self.title,
            'animal_id': self.animal_id,
            'questions': self.questions,
            'answer_sheets': self.answer_sheets
        }
        
    @staticmethod
    def form_helper(form)->dict:
        return {
            "id": str(form["_id"]),
            "title": form ["title"],
            "animal_id": str(form["animal_id"]),
            "questions": form["questions"],
            "answer_sheets": form["answer_sheets"]
        }
        