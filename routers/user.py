from fastapi import APIRouter
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi.responses import JSONResponse

user_router = APIRouter()

# Clase Usuari
class User(BaseModel): 
    email: str 
    password: str

#LOGIN
@user_router.post('/login', tags=['Auth']) 
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict()) 
        return JSONResponse(content=token, status_code=200) 
    return JSONResponse(status_code=400,content='User or password invalido')
