from fastapi import FastAPI,APIRouter, Body, HTTPException, Path, Query, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import *
from BD.database import Base, Session, motor
from Modelos.modelos import Movie as Mv

class BearerJWT(HTTPBearer):
    async def   __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validarToken(auth.credentials)
        if data['email'] != 'ejemplo@gmail.com':
            raise HTTPException(status_code=403,detail='Credenciales incorrectas')
        
        
class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    overview: str = Field(min_length=10, max_length=30)
    year: int =Field(default=1950)
    rating: float = Field(ge=1,le=10)
    category: str = Field(min_length=5,max_length=40)


routerMovie = APIRouter()



@routerMovie.get('/',tags=['Metodo Inicial'])

@routerMovie.get('/movies',tags=['Get Movies'], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    data = db.query(Mv).all()

    return JSONResponse(content=jsonable_encoder(data) )

#get con parametro
@routerMovie.get('/movies/{id}',tags=['Get Movie'])
def get_movie(id:int = Path(ge=1,le=100)):
    db = Session()
    data = db.query(Mv).filter(Mv.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'Recurso no existe'})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

#get con query
@routerMovie.get('/movies/',tags=['Get Movie con query'])
def get_movies_category(category:str = Query(min_length=3,max_length=100)):
    db = Session()
    data = db.query(Mv).filter(Mv.category == category ).all()
    if data:
        return JSONResponse(status_code=200, content=jsonable_encoder(data))
    else:
        return JSONResponse(status_code=404, content={'message': 'Recurso no existe'})
    

@routerMovie.post('/movies', tags=['Agregar Movie'])
def post_movie(movie: Movie):
    db = Session()
    newMv = Mv(**movie.dict())
    db.add(newMv)
    db.commit()
    return JSONResponse(content={'message':'Se ha cargado una nueva pelicula'})

@routerMovie.put('/movies/{id}', tags=['Actualizar Movie'])
def act_movie(id: int, movie:Movie):
    db = Session()
    data = db.query(Mv).filter(Mv.id == id).first()
    if data:
        data.title = movie.title
        data.overview = movie.overview
        data.year = movie.year
        data.rating = movie.rating
        data.category = movie.category
        db.commit()
        return JSONResponse(status_code=200, content=jsonable_encoder(data))
    else:
        return JSONResponse(status_code=404, content={'message': 'Recurso no existe'})
    
@routerMovie.delete('/movies/{id}', tags=['Eliminar Movie'])
def eliminar_movie(id:int):
    db = Session()
    data = db.query(Mv).filter(Mv.id == id).first()
    if data:
        db.delete(data)
        db.commit()
        return JSONResponse(status_code=200, content={'message': 'Recurso eliminado'})
    else:
        return JSONResponse(status_code=404, content={'message': 'Recurso no existe'})