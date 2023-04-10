#CODIGO COMENTADO INTRODUCTORIO EN LA RAMA INTRO
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse 
from pydantic import BaseModel, Field 
from typing import Optional, List 
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Base, session, engine
from models.movie import Movie as MovieModel 
from fastapi.encoders import jsonable_encoder 
from middlewares.error_handler import ErrorHandler #Importamos nuestro manejador de errores

app = FastAPI() 
app.title = 'Mi First API con FastAPI' 
app.version = '0.0.1' 

app.add_middleware(ErrorHandler)

#Aquí creamos todas las Tablas generadas en nuestro modelo
Base.metadata.create_all(bind=engine)

# Clase Usuari
class User(BaseModel): 
    email: str 
    password: str

# Autentificación de Token
class JWTBearer(HTTPBearer): 
    async def __call__(self, request: Request): 
        auth = await super().__call__(request) 
        data = validate_token(auth.credentials) 
        if data['email'] != 'admin@gmail.com': 
            raise HTTPException(status_code=403, detail='Credenciales invalidas')

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


#GET HOLA MUNDO
@app.get('/', tags=['HOME']) 
def message():
    return HTMLResponse('<h1>HOLA MUNDO</h1>')

#LOGIN
@app.post('/login', tags=['Auth']) 
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict()) 
        return JSONResponse(content=token, status_code=200) 
    return JSONResponse(status_code=400,content='User or password invalido')

#MOVIE LIST
movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Duro de Matar',
        'overview': "Un policia de NY llega al Nacatomi Plaza para ver a su ex esposa e hijos por navidad y termina en un secuestro terrorista ...",
        'year': '1988',
        'rating': 9.4,
        'category': 'Acción'    
    } 
]

#GET MOVIE
@app.get('/movies',tags=['MOVIES'], status_code=200, response_model=List[Movie], dependencies=[Depends(JWTBearer())]) 
def get_movies():
    db = session()
    result = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(result)) 

#GET MOVIE FOR ID
@app.get('/movies/{id}', tags=['MOVIES'], dependencies=[Depends(JWTBearer())])
def get_movie(id: int = Path(ge=1,le=2000)) -> Movie:     
    db = session()
    result =  db.query(MovieModel).filter(MovieModel.id == id).first()    
    if not result:        
        return JSONResponse(status_code = 404, content='ID invalido')
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

#GET MOVIE BY CATEGORY
@app.get('/movies/', tags=['MOVIES'], response_model = List[Movie], dependencies=[Depends(JWTBearer())]) 
def get_movies_by_category(category: str =  Query(min_length = 5, max_length =15 )):
    db = session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content='Invalid Category')
    return JSONResponse(status_code=200 ,content=jsonable_encoder(result))

#POST MOVIE
@app.post('/movies', tags=['MOVIES'], response_model= dict, dependencies=[Depends(JWTBearer())]) 
def create_movie(movie: Movie):
    db = session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code = 201, content='Se ha registrado la pelicula') 

#PUT MOVIE FOR ID
@app.put('/movies/{id}', tags=['MOVIES'], response_model= dict, status_code = 200, dependencies=[Depends(JWTBearer())])
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
@app.delete('/movie{id}', tags=['MOVIES'], response_model= dict, status_code = 200, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int):
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content='ID invalido')
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200,content= 'Se ha eliminado la pelicula')
    









