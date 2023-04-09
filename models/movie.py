#Aqui crearemos la Clase (Class), que servira como plantilla para nuestra Tabla de peliculas.
from config.database import Base
from sqlalchemy import column, Integer, String, Float # Importamos las Calses (class), que utilisaremos para definir los tipos de datos de las columnas y tambien definir las columnas.

# Importante: Al ser clases cada una tendra funcionalidades correspondientes al tipo de dato que corresponde.

# Primero definimos la Tabla (Todo esto esta basado en POO)
class Movie(Base): # Heredamos de la base modelo 'base' instaurada en DATABASE.
    __tablename__ = 'movies'
    # __tablename__ : Es una convencion de SQLAlchemy para definir como atributo el nombre de la Tabla. (No es una palabra reservada, sino mas bien un atributo de la base modelo (base), en la que se almacena el nombre de la tabla)
    #OBS: El nombre no debe contener espaciado sino se utiliza los ( _ )

    id = column(Integer , primary_key = True)
    # Con 'column' definimos que es una columna, con 'Integer' el tipo de dato entreo y con 'primary_key' definimos que es la clave primari (Con lo que identificamos de manera unica cada registro).

    title = column(String)
    overview = column(String)
    year = column(Integer)
    rating = column(Float)
    category = column(String)