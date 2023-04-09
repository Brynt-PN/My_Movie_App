
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse 
from pydantic import BaseModel, Field 
from typing import Optional, List 
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import Base, session, engine #Importamos las clases de nuestra BD
from models.movie import Movie as MovieModel #Importamos la clase Movie como MocieModel para que no se cruce con la clase Movie de la linea 34
from fastapi.encoders import jsonable_encoder #Importamos esto para poder convertir un objeto en una respuesta con formato JSON (Linea 96)

app = FastAPI() 
app.title = 'Mi First API con FastAPI' 
app.version = '0.0.1' 

#Aquí creamos todas las Tablas generadas en nuestro modelo
Base.metadata.create_all(bind=engine) # Subdividimos en lo siguiente:
# BASE : Esta es la clase que instauramos anteriormente de Declarative_base, que sirve para crear Tablas en la BD
# METADATA : Este es un objeto que BASE (declarative_base) ya tiene incorporado y que contiene la informacipon de las tablas creadas a partir de BASE (HEREDAN)
# CREATE_ALL : Es un metodo de METADATA que crea todas las tablas que heredan de BASE que aun no han sido creadas.

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
    #Creamos una session para la consulta
    db = session()
    #Usamos el metodo QUERY de SQLAlchemy para consultar el contenido de la tabla
    result = db.query(MovieModel).all()
    #El metodo QUERY recive como parametro la tabla a consultar.
    #El metodo ALL indica que se muestre todos los registros de una TABLA.

    return JSONResponse(content=jsonable_encoder(result)) #Aqui usamos 'jsonable_encoder' para darle formato JSON a la lista de objetos resultantes.

#GET MOVIE FOR ID
@app.get('/movies/{id}', tags=['MOVIES'], dependencies=[Depends(JWTBearer())])
def get_movie(id: int = Path(ge=1,le=2000)) -> Movie: 
    # Creamos una Instarncia de Session
    db = session()
    #Aacemos una consulta a la BD y filtramos
    result =  db.query(MovieModel).filter(MovieModel.id == id).first()
    #QUERY : Hacemos la consluta a la TABLA
    #FILTET : Filtramos y pasamos los parametros de filtro, en este caso indicamos que 'MocieModel.id' (El parametro id del objeto) debe ser igual a 'id' (El parametro que recive este metodo GET '(id: int = Path(ge=1,le=2000))' )
    #FIRST : Indica que devuelva el primer resultado o coincidencia.

    #Validamos que el resultado no este vacio
    if not result:
        #Devolvemos un mensaje de error.
        return JSONResponse(status_code = 404, content='ID invalido')
    #Devolvemos el resultado obtenido y lo pasamos con formato JSON
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

#GET MOVIE BY CATEGORY
@app.get('/movies/', tags=['MOVIES'], response_model = List[Movie], dependencies=[Depends(JWTBearer())]) 
def get_movies_by_category(category: str =  Query(min_length = 5, max_length =15 )):
    db = session()
    #A diferencia del ejemplo anterior en filtrado por ID, usamos ALL y no First, por que queremos que nos devulva todos las peliculas de la categoria que ingresemos.
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        return JSONResponse(status_code=404, content='Invalid Category')
    return JSONResponse(status_code=200 ,content=jsonable_encoder(result))

#POST MOVIE
@app.post('/movies', tags=['MOVIES'], response_model= dict, dependencies=[Depends(JWTBearer())]) 
def create_movie(movie: Movie):
    #Ahora agregaremos la nueva pelicula a la BD

    #Primero abrimos una session (Una conección temporal a la BD)
    db = session() # Aqui isnstauramos de la clase Session

    #Instauramos de la calse MOVIEMODEL un nuebo objeto y lo guardamos en una variable
    new_movie = MovieModel(**movie.dict()) # Aqui subdividimos:
    #movie : Recordemos que el parametro movie lo instauramos a partir de la clase Movie '(movie: Movie)'
    #.dict() : Aqui convertimos al objeto en un diccionario.
    # ** : Con este Operador de Python desempaquetamos los valores del diccionario y lo obtenemos en el formato (Clave='Valor'), esto nos ayuda a poder pasar el contenido de un diccionario como parametros de una función o en este caso de una clase.
    # OBS: Para que '**' funcione, las claves del Dic deben coincidir con el nombre de los aprametros que requiere la clase o función, de otro modo botara error.

    #Añadimos la Nueva pelicula a la BD,  recordemos que 'bd' es una instaciá de la session, es decir una conexión temporal a la BD
    db.add(new_movie)

    #Guardamos los cambios realizados
    db.commit()

    #IMPORTANTE : Si los cambios no se guardan, solo permaneceran durante la session y no podran ser vistos desde otras sessiones diferentes.

    return JSONResponse(status_code = 201, content= {'message':'Se ha registrado la pelicula'}) 

#PUT MOVIE FOR ID
@app.put('/movies/{id}', tags=['MOVIES'], response_model= dict, status_code = 200, dependencies=[Depends(JWTBearer())])
def update_movies(id: int, movie: Movie): 
    for item in movies: 
        if item['id'] == id: 
            item['title'] = movie.title 
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category 
            return JSONResponse(content= {'message':'Se ha modificado la pelicula'})
    return JSONResponse(status_code = 404, content='ID invalido')

#DELETE MOVIE FOR ID
@app.delete('/movie{id}', tags=['MOVIES'], response_model= dict, status_code = 200, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int):
    for item in movies: 
        if item['id'] == id: 
            movies.remove(item)
            return JSONResponse(content= {'message':'Se ha eliminado la pelicula'})
    return JSONResponse(status_code = 404, content='ID invalido')










