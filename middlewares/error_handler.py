from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse

#Creamos una clase que manejara los posibles errores en nuestras Rutas
class ErrorHandler(BaseHTTPMiddleware): # Hereda de 'BaseHTTPMiddleware'

    #Definimos el constructor que recive como parametro la APP que sera de tipo FASTAPI
    def __init__(self, app: FastAPI) -> None:
        #Accdedemos a la clase padre con 'super()' y a su constructor que recibe la APP como parametro.
        super().__init__(app)
    
    #Aqui creamos nuestro manejador de errores con la función 'dispatch'
    async def dispatch(self, request: Request, call_next) -> Response or JSONResponse:
        # Reques : Nuestra solicitud HTTP
        # dispach : función que nos permite llamar a la siguinete 'middleware'
        # middleware : Pedasos de código por los que pasa nuestra solicitud HTTP antes de llegar al operador que dara respuesta
        # call_nest : Llama al siguiente 'middleware' en la cadena.
        # async : Indica que esta función se ejcuta en segundo Plano, mientras se continua ejecuntando otras.

        #Generamos un bloque TRY EXCEPT para manejo de errores.
        try:
            return await call_next(request)
            # return : Es lo que retorna nuestra función
            # Await : Indica que esto se ejecuta mientras esperamos que se termine con la funcipon asyncrona (async).
            # call_next(request) : Pasamos al siguiente 'middleware', le pasamos el parametro request, se puede ejecutar corectamenete o puede recivir un error

            #Se almacena el error (Exception), en caos haya uno.
        except Exception as e:
            #Se muestra el mensaje de error
            return JSONResponse(status_code=500, content={'error': str(e)})