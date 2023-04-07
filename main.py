#CODIGO COMENTADO DE INTRODUCCIÓN EN LA RAMA INT
#CODIGO COMENTADO DE INTERMEDIO EN LA RAMA MED
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse 
from pydantic import BaseModel, Field 
from typing import Optional, List 
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI() 
app.title = 'Mi First API con FastAPI' 
app.version = '0.0.1' 

# Creamos una Clase USUARIO par que se pueda registrar
class User(BaseModel): 
    email: str # Pasamos los parametros 'email' y 'password' 
    password: str

#Creamos una clase que hereda de HTTPBEARER, esto nos permitira obtener el toquen en una solicitud del usuario luego que este se haya registrado (Ruta LOGIN)
class JWTBearer(HTTPBearer): # Usaremos una funcion '__call__' para poder llamar al objeto instaurado como función( es decir se ejecutara llamado al objeto y pasando parametros si es que se requiere 'OBJETO(PARAMETROS)')
    async def __call__(self, request: Request): # Nuestra primera funcion CALL solicita un parametro 'request' que lo instauramos como un objeto de la calse 'REQUEST' que importamos de 'FASTAPI'

        # IMPORTANTE: El parametro 'Request' representa la solicitud HTTP y al instaurarlo como un objeto 'REQUEST' podemos accder a las cabeceras de la solicitud incluida la parte donde se encuentra el TOKEN de seguridad. Las siguientes lineas de código se dedican a ello.

        auth = await super().__call__(request) # De la clase padre 'HTTPBearer' llamamos su propia funcion CALL para acceder a ella usamos la clase 'super().' y al final pasamos el parametro 'Request', todo lo guardamos dentro de la variable 'auth' (Esto en resumen nos devuelve las credenciales de la solicitud).
        data = validate_token(auth.credentials) # Accedemos a las credeciales de AUTH y lo pasamos por nuestra funcion VALIDATE_TOKEN que nos devuleve los datos cifrados en forma de Diccionario (Estos datos son el email y el password que se cifraron en el token al hacer login).
        if data['email'] != 'admin@gmail.com': # Comprobamos que sean correctos, en caso contrario se devolvera un mensaje de Credenciales ivalidas.
            raise HTTPException(status_code=403, detail='Credenciales invalidas')

class Movie(BaseModel):
    id: Optional[int] = None 
    title: str = Field(default= 'Mi Pelicula', min_length= 5, max_length= 15)
    overview: str = Field(min_length= 15, max_length= 50)
    year: int = Field(le= 2024) 
    rating: float = Field(ge = 1, le= 10)
    category: str 

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



@app.get('/', tags=['HOME']) 
def message():
    return HTMLResponse('<h1>HOLA MUNDO</h1>')

@app.post('/login', tags=['Auth']) # Creamos la ruta Login para que se registre
def login(user: User):# Creamos la función eh istanciamos el parametro user en la clase User ( user: User).
    if user.email == 'admin@gmail.com' and user.password == 'admin': # En la calse User, se compone de 'email' y 'password', aqui con un IF validamos que sus valores sean los correctos.
        token: str = create_token(user.dict()) # Si son correctos los pasamos por nuestra funciín 'create_token' para crear un token de autentifivavión.
        return JSONResponse(content=token, status_code=200) # Retornamos es token
    return JSONResponse(status_code=400,content='User or password invalido')

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


@app.get('/movies',tags=['MOVIES'], status_code=200, response_model=List[Movie]) #Podemos añadir el 'codigo de estado' que queremos que ejecute esta petición cunado se procese bien
def get_movies():
    return JSONResponse(content=movies) 

@app.get('/movies/{id}', tags=['MOVIES'])
def get_movie(id: int = Path(ge=1,le=2000)) -> Movie: 
    for item in movies:
        if item['id'] == id:
            return JSONResponse(content=item) 
    return JSONResponse(status_code = 404, content='ID invalido')

@app.get('/movies/', tags=['MOVIES'], response_model = List[Movie], dependencies=[Depends(JWTBearer())]) # Protegeremos esta Ruta usando el parametro dependencies, que recive una lista de dependencias dentro de la cual le pasamos la funcion DEPENDS que importamos de FASAPI y a la cual le pasamos la classe que se ejecutara en este caso seria JWTBearer.
#Aqui el parametro request de la clasee JWTBearer representa la solicitud HTTP y se ejecuta antes de la funcion GET_MOVIES_BY_CATEGORY, 'Request' Contiene la info de la solictud incluida la cabeceda de seguridad que tiene el TOKEN
def get_movies_by_category(category: str =  Query(min_length = 5, max_length =15 )):
    data = [item for item in movies if item['category'] == category]
    return JSONResponse(status_code=200 ,content=data)

@app.post('/movies', tags=['MOVIES'], response_model= dict) 
def create_movie(movie: Movie): 

    movies.append(movie) 
    return JSONResponse(status_code = 201, content= {'message':'Se ha registrado la pelicula'}) #Tambien podemos indica el 'codigo de estado' desde la respuesta

@app.put('/movies/{id}', tags=['MOVIES'], response_model= dict, status_code = 200)
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

@app.delete('/movie{id}', tags=['MOVIES'], response_model= dict, status_code = 200)
def delete_movie(id: int):
    for item in movies: 
        if item['id'] == id: 
            movies.remove(item)
            return JSONResponse(content= {'message':'Se ha eliminado la pelicula'})
    return JSONResponse(status_code = 404, content='ID invalido')










