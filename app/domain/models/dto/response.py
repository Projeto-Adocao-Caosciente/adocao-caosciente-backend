# TODO: Criar um DTO de retorno padrão para todas as rotas

# NOTE: O status não é retornado mas vai ser utilizado para mapear futuros erros (deve-se criar pasta errors)
class ResponseDTO():
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.data = data

    def __dict__(self):
        return {
            'message': self.message,
            'data': self.data
        }