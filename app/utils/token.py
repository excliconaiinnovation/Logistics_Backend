from datetime import datetime, timedelta
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM

def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=15)
    payload = {
        "sub": email,
        "exp": expire,
        "type": "reset"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "reset":
            return None
        return payload.get("sub")
    except:
        return None