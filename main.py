#CODIGO COMENTADO INTRODUCTORIO EN LA RAMA INTRO
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import Base, engine
from middlewares.error_handler import ErrorHandler #Importamos nuestro manejador de errores
from routers.movie import movie_router #Importamos el enrutador
from routers.user import user_router

#Instanciamos la APP
app = FastAPI() 
app.title = 'Mi Movie App' 
app.version = '0.0.3' 

#Añadimos el controlador de errores
app.add_middleware(ErrorHandler)
# add_middleware : Metodo para agregar un middñeware
# ErrorHandler : Nuestro manejador de errores

#Añadimos el Router Movie
app.include_router(movie_router) #Usamos 'include_router' para agregar el enrutador
app.include_router(user_router)

#Aquí creamos todas las Tablas generadas en nuestro modelo
Base.metadata.create_all(bind=engine)

#GET HOLA MUNDO
@app.get('/', tags=['HOME']) 
def message():
    return HTMLResponse('<h1>HOLA MUNDO</h1>')


#Cambio de Prueba





