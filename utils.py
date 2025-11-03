import jwt
from datetime import datetime, timedelta, timezone
from redis_client import r

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

#生成JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    # === 将 Token 存入 Redis (key=username, value=token) ===
    username = data["username"]
    r.set(f"token:{username}", token, ex=1800)
    return token

#验证JWT
def verity_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")

        # === 从 Redis 验证 Token 是否有效 ===
        redis_token = r.get(f"token:{username}")
        if redis_token != token:
            return {"error":"Token 已失效或被强制下线"}

        return payload
    except jwt.ExpiredSignatureError:
        return {"error":"Token过期"}
    except jwt.InvalidTokenError:
        return {"error":"无效Token"}

def logout(username: str):
    r.delete(f"token:{username}")
    return {"msg":f"{username} 已登出"}
