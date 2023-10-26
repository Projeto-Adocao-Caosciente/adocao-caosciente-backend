import json
from fastapi import FastAPI
from app.routes import ong_route, animal_route, login_route

api = FastAPI(
    title="Adoção Cãosciente",
    version="0.1.0"
)

api.include_router(ong_route.router)
api.include_router(animal_route.router)
api.include_router(login_route.router)

# TODO: Todas as services devem retornar um DTO padrão com mensagem de erro, status e dado. dessa forma 
# a rota se preocupa apenas em retornar o DTO e não precisa se preocupar com o status code

@api.on_event("startup")
async def startup_event():
    with open("docs/swagger_dump.json", "w") as fp:
        fp.write(json.dumps(api.openapi()))
