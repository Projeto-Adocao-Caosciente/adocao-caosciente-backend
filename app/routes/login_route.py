from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
import time

from app.domain.models.login import LoginModel
from app.services.login_service import LoginService

router = APIRouter(
    prefix="/login",
    tags=['login']
)

# JWT_SECRET = config("secret")
# JWT_ALGORITHM = config("algorithm")

JWT_SECRET = "BANANA"
JWT_ALGORITHM = "HS256"

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "user_roles": {
            "ONG": True,
        },
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=400, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid

login_service = LoginService()

@router.post("/", status_code=200)
async def login(
    login: LoginModel,
    authorization: str = Header(None),
):
    # return signJWT('joao@mailinator.com')
    ong = login_service.authenticate(login.cnpj, login.password)

    if ong is None:
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    
    return signJWT(ong["email"])