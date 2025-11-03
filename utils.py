import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

#生成JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#验证JWT
def verity_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error":"Token过期"}
    except jwt.InvalidTokenError:
        return {"error":"无效Token"}

