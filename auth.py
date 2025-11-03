from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import create_access_token

router = APIRouter()

fake_user = {
    "username": "admin",
    "password": "123456"
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(user: LoginRequest):
    if user.username == fake_user["username"] and user.password == fake_user["password"]:
        token = create_access_token({"username": user.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401,detail="用户名或密码错误")
