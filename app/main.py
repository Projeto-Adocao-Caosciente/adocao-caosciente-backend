import http
import json
import logging.config
import random
import string
import time
from fastapi import FastAPI
from app.routes import ong_route, animal_route, auth_route, adopter_route, form_route
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings

from app.domain.models.dto.response import ResponseDTO
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

api = FastAPI(
    title="Adoção Cãosciente",
    summary="API para um sistema de automação de adoção de animais para uma ONG",
    
    license_info={
        "name": "MIT License",
        "url": "https://github.com/Projeto-Adocao-Caosciente/adocao-caosciente-backend/blob/e949baef1332d573e77a7d2103c7c7ec5e266854/LICENSE"
    },
    contact={
        "name": "Support Team",
        "url": "https://adocao-caosciente-frontend.vercel.app/contact",
    },
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
api.include_router(auth_route.router)
api.include_router(form_route.router)
api.include_router(adopter_route.router)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

@api.on_event("startup")
async def startup_event():
    env = settings.ENVIRONMENT
    if env == "test":
        raise Exception("You are running tests. Database will not be created.")

    with open("docs/swagger_dump.json", "w") as fp:
        fp.write(json.dumps(api.openapi()))


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    custom_error = [f"{error['loc'][1]}: {error['msg']}" for error in exc.errors()]
    return JSONResponse(
        status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
        content=ResponseDTO(custom_error, "Validation Fields Errors", http.HTTPStatus.UNPROCESSABLE_ENTITY).dict()
    )

@api.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
        content=ResponseDTO(None, repr(exc), http.HTTPStatus.INTERNAL_SERVER_ERROR).dict()
    )

@api.middleware("http")
async def log_requests(request, call_next):
    request_id: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    request.state.request_id = request_id
    logger = logging.LoggerAdapter(logging.getLogger(__name__), {"request_id": request_id})
    logger.info(f"Request<{request_id}> start request path={request.url.path} method={request.method}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{:.2f}".format(process_time)
    logger.info(f"id={request_id} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response