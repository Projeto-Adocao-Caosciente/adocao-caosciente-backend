import time
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Request
import jwt
import time

# TODO: definir como variavel de ambiente
JWT_SECRET = "BANANA"
JWT_ALGORITHM = "HS256"


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.credentials = None

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=400, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            self.credentials = credentials.credentials
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=401, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        payload = None
        try:
            payload = self.decode_jwt(jwtoken)
        except Exception as e:
            print("Error decoding token: ", e)

        return True if payload else False

    def decode_jwt(self, jwt_token: str):
        try:
            payload = jwt.decode(jwt_token, JWT_SECRET,
                                 algorithms=[JWT_ALGORITHM])
            return payload
        except Exception as e:
            print("Error decoding token: ", e)
            return None

    def get_user_id(self) -> str:
        token = self.credentials
        payload = self.decode_jwt(token)
        return payload["user_id"]

    def get_user_roles(self) -> dict:
        token = self.credentials
        payload = self.decode_jwt(token)
        return payload["user_roles"]

    def refresh_jwt(self) -> str:
        token = self.credentials
        payload = self.decode_jwt(token)
        payload["expires"] = time.time() + 3600
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return token

    @staticmethod
    def sign_jwt(user_id: str, role: str) -> str:
        payload = {
            "user_id": user_id,
            "user_roles": {
                role: True
            },
            "expires": time.time() + 3600
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return token
