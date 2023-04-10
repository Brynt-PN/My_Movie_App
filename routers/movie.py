from fastapi import APIRouter # Importamos para crear nuestro ROUTER 

# Instanciamos nuestro ENRUTADOR, que manejara las rutas para nuestras peliculas y asi las podemos definir de manera modular, manteniendo el código mas ordenado.
movie_router = APIRouter()


#Aqui importamos lo necesario para nuestras rutas Movie
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse 
from pydantic import BaseModel, Field 
from typing import Optional, List 
from config.database import  session
from models.movie import Movie as MovieModel 
from fastapi.encoders import jsonable_encoder 
from middlewares.jwt_bearer import JWTBearer#Lo agregamos a la carpeta Middleware y ahora lo importamos desde ahí (Mantener un orden)


#Aqui agregamos todas las rutas relacionadas a MOVIE

# OBS : Todas las rutas ahora usan 'movie_router' en lugarde 'app'

#Calse Movie 
class Movie(BaseModel):
    id: Optional[int] = None 
    title: str = Field(default= 'Mi Pelicula', min_length= 5, max_length= 15)
    overview: str = Field(min_length= 15, max_length= 500)
    year: int = Field(le= 2024) 
    rating: float = Field(ge = 1, le= 10)
    category: str 

    #Configuración predeterminada de Movie
    class Config:
        schema_extra = {
            'example': {
                'id' : 0,
                'title':'Mi pelicula',
                'overview':'Descripcíon de la Pelicula',
                'year': 2022,
                'rating' : 5.5,
                'category' : 'Acción'
            }
        }

#GET MOVIE
@movie_router.get('/movies',tags=['MOVIES'], status_code=200, response_model=List[Movie], dependencies=[Depends(JWTBearer())]) 
def get_movies():
    db = session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result)) 

#GET MOVIE FOR ID
@movie_router.get('/movies/{id}', tags=['MOVIES'], dependencies=[Depends(JWTBearer())])
def get_movie(id: int = Path(ge=1,le=2000)) -> Movie:     
    db = session()
    result =  db.query(MovieModel).filter(MovieModel.id == id).first()    
    if not result:        
        return JSONResponse(status_code = 404, content='ID invalido')
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

#GET MOVIE BY CATEGORY
@movie_router.get('/movies/', tags=['MOVIES'], response_model = List[Movie], dependencies=[Depends(JWTBearer())]) 
def get_movies_by_category(category: str =  Query(min_length = 5, max_length =15 )):
    db = session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content='Invalid Category')
    return JSONResponse(status_code=200 ,content=jsonable_encoder(result))

#POST MOVIE
@movie_router.post('/movies', tags=['MOVIES'], response_model= dict, dependencies=[Depends(JWTBearer())]) 
def create_movie(movie: Movie):
    db = session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code = 201, content='Se ha registrado la pelicula') 

#PUT MOVIE FOR ID
@movie_router.put('/movies/{id}', tags=['MOVIES'], response_model= dict, status_code = 200, dependencies=[Depends(JWTBearer())])
def update_movies(id: int, movie: Movie):
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content='ID invalido')
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(content= {'message':'Se ha modificado la pelicula'})
    

#DELETE MOVIE FOR ID
@movie_router.delete('/movie{id}', tags=['MOVIES'], response_model= dict, status_code = 200, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int):
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content='ID invalido')
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200,content= 'Se ha eliminado la pelicula')
    