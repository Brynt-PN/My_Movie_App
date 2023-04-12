from pydantic import BaseModel


# Clase Usuari
class User(BaseModel): 
    email: str 
    password: str