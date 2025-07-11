from fastapi import Request, HTTPException
from app.auth.jwt import verify_token
from jwt import ExpiredSignatureError, InvalidTokenError

def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    token = auth_header.split(" ")[1]

    try:
        payload = verify_token(token)

        if "email" not in payload or "role" not in payload:
            raise HTTPException(status_code=401, detail="Token sin campos requeridos")

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
