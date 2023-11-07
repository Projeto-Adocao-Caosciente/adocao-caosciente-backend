import json
from fastapi import FastAPI, Response
from app.routes import ong_route, animal_route, login_route
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI(
    title="Adoção Cãosciente",
    version="0.1.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://adocao-caosciente-frontend.vercel.app",
    "https://adocao-caosciente-frontend.vercel.app",
]

headers = [
    "X-CSRF-Token", 
    "X-Requested-With",
    "Accept",
    "Accept-Version",
    "Content-Length",
    "Content-MD5",
    "Content-Type",
    "Date",
    "X-Api-Version",
    "Authorization"
]

# TODO: Verificar headers e definir melhor isso para garantir segurança como o no-sniff, xss, etc

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=headers,
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

@api.middleware("http")
async def pass_options_request(request, call_next):
    if request.method == "OPTIONS":
        return Response(status_code=204)
    return await call_next(request)