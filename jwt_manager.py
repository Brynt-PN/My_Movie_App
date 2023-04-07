# En este archivo crearemos la función generadora del token de validación para la autenticación de la cuenta.
from jwt import encode, decode # Importamos de JWT la clase ENCODE y DECODE

'''IMPORTANTE: 
1 -El servidor genera un token JWT utilizando la información del usuario que se desea autenticar. Este token contiene una firma digital que garantiza su autenticidad.

2 -El servidor envía el token JWT al cliente, que lo almacena en el navegador o en la aplicación.

3- El cliente envía el token JWT al servidor en cada solicitud que realiza. El servidor puede verificar la firma del token para asegurarse de que proviene de un emisor válido y que no ha sido modificado.

4 -Si la firma es válida, el servidor utiliza la información almacenada en el token JWT     para autenticar al usuario y autorizar su acceso a los recursos solicitados.'''

def create_token(data: dict) -> str: # Definimos la función para crear el token y le pasamos un parametro 'DATA' que contrendra todo la info necesaria para crear el token, y definimos que tendra formato de DICCIONARIO.
    token: str = encode(payload=data, key='1998', algorithm='HS256') # Aqui definimos una variable 'TOKEN' indicamos que es de tipo 'STRING' y la instauramos con la Clase 'ENCODE' y le pasamos los parametros 'pyload' es el contenido que queremos guardar dentro del token 'DATA', 'key' que es una cadena secreta utilizada para firmar el token (debe ser un string y servira para desifrar el token), 'algorithm' que es el algoritmo de cifrado utilizado para firmar el token. En este caso, se utiliza el algoritmo "HS256" (que lo sugiere directamente el programa)
    return token # Retornamos el valor de 'TOKEN'

def validate_token(token: str) -> dict: # Definimos una función para validar el token usado DECODE.
    data: dict = decode(token, key='1998', algorithms=['HS256'])# Aqui definimos una variable 'DATA' indicamos que es de tipo 'DICTIONARY' y la instauramos con la Clase 'DECODE' y le pasamos los parametros 'token' es el token que queremos validar, 'key' que es una cadena secreta utilizada para firmar el token (debe ser la misma que utilizamos para firmar el token), 'algorithms' en este caso es una lista y en ella esta los algoritmos utilizados para firmar el token, en este caso solo 'HS256'.
    return data