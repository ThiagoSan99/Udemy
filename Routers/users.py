from fastapi import APIRouter, FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from user_jwt import *

login_user = APIRouter()

##Usuario
class User(BaseModel):
    email: str
    password : str


##Usuario
@login_user.post('/login', tags=['autenticación'])
def login(user: User):
    if user.email == 'ejemplo@gmail.com'and user.password == '123':
        token: str = crearToken(user.dict())
        print(token)
        return JSONResponse(content=token)


