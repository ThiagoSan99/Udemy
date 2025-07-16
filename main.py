from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from user_jwt import *
from BD.database import Base, motor
from Routers.movie import *
from Routers.users import *


Base.metadata.create_all(bind=motor)


def leer_root():
    return HTMLResponse('<h3> Aprendiendo fastAPI<h3>')

movies = [
 {
     'id':1,
     'title':'Jurasicc park',
     'overview':'Pelicula sobre dinosaurios',
     'year':'1990',
     'rating':9.1,
     'category':'CiFy'
 }   
]


#descripción de la interfaz de la API
app = FastAPI(
    title="FastAPI",
    description="Primera API"

)

app.include_router(routerMovie)



