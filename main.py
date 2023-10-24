from fastapi import FastAPI
import json

from routes import ong_route, animal_route, login_route

api = FastAPI(
    title="Adoção Cãosciente",
    version="0.1.0"
)

api.include_router(ong_route.router)
api.include_router(animal_route.router)
api.include_router(login_route.router)

@api.on_event("startup")
async def startup_event():
    with open("docs/swagger_dump.json", "w") as fp:
        fp.write(json.dumps(api.openapi()))

@api.get('/')
async def root():
    return {"message": "Hello World from Adoção Cãosciente"}
