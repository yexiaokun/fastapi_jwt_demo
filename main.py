from fastapi import FastAPI, Depends, HTTPException, Header
from auth import router as auth_router
from utils import verity_token

app = FastAPI(title="JWT Login Demo")

app.include_router(auth_router)

@app.get("/protected")
def protected_route(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=401,detail="未提供Token")
    
    token = Authorization.replace("Bearer ","")
    result = verity_token(token)

    if "error" in result:
        raise HTTPException(status_code=401,detail=result["error"])
    
    return {"msg":"欢迎访问受保护接口", "user": result["username"]}
