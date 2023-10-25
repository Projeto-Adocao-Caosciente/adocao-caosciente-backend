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

@api.on_event("startup")
async def startup_event():
    with open("docs/swagger_dump.json", "w") as fp:
        fp.write(json.dumps(api.openapi()))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000, reload=True)
