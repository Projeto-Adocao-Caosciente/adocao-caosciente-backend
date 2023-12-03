from typing import List
from pydantic import BaseModel

# TODO: Mandar para outro arquivo depois
class Choice(BaseModel):
    id: int
    label: str
    is_correct: bool

class Question(BaseModel):
    question: str
    choices: List[Choice]

class FormModel(BaseModel):
    title: str = None
    animal_id: str = None
    questions: List[Question] = []
    answer_sheets: List[str] = []

    def required_field_at_create(self) -> set:
        return {"title", "questions"}
    
    class Config:
        json_schema_extra = {
            "title": "Questionario",
            "questions": [
                {
                    "question": "Essa é uma pergunta?",
                    "choices": [
                        {"id":0,"label":"Sim", "is_correct":True},
                        {"id":1,"label":"Não", "is_correct":False},
                        {"id":2,"label":"É Sim", "is_correct":True},
                    ]
                },
                {
                    "question": "Voce Mora em:",
                    "choices": [
                        {"id":0,"label":"Casa", "is_correct":True},
                        {"id":1,"label":"Apartamento", "is_correct":True},
                        {"id":2,"label":"Van", "is_correct":False},
                    ]
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
    def helper(form)->dict:
        return {
            "id": str(form["_id"]),
            "title": form ["title"],
            "animal_id": str(form["animal_id"]),
            "questions": form["questions"],
            "answer_sheets": form["answer_sheets"]
        }
        