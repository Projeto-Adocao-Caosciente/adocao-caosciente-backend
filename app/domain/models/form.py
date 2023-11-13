from pydantic import BaseModel, Field
class FormModel(BaseModel):
    animal_id: str = ""
    questions: list = []
    answer_sheets: list[str] = []
    
    class Config:
        schema_extra = {
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
            'animal_id': self.animal_id,
            'questions': self.questions,
            'answer_sheets': self.answer_sheets
        }
        
    @staticmethod
    def form_helper(form)->dict:
        return {
            "id": str(form["_id"]),
            "animal_id": str(form["animal_id"]),
            "questions": form["questions"],
            "answer_sheets": form["answer_sheets"]
        }
        