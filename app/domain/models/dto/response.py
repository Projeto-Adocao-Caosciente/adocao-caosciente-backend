# TODO: Criar um DTO de retorno padrão para todas as rotas

# NOTE: O status não é retornado mas vai ser utilizado para mapear futuros erros (deve-se criar pasta errors)
import http
from typing import Callable


class ResponseDTO():
    def __init__(self, data, message, status):
        self.status = status
        self.message = message
        self.data = data

    def dict(self):
        return {
            'message': self.message,
            'data': self.data
        }
    

def duplicate_key_response(key: str, match_field: Callable[[str], str]) -> ResponseDTO:
    return ResponseDTO({"field": {
                "key": key,
                "value": match_field(key)
            }}, key + " already in use", http.HTTPStatus.CONFLICT)
