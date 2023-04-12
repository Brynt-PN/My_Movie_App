from pydantic import BaseModel, Field
from typing import Optional

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