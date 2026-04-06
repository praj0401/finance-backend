from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

security = HTTPBearer()


def get_current_user(token=Depends(security)):
    try:
        token_str = token.credentials.strip()  # important fix

        payload = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])

        return payload

    except Exception as e:
        print("JWT ERROR:", str(e))  # debug print
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def role_required(allowed_roles: list):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return checker