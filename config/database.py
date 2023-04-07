import os #Esto es de la biblioteca standart de Python y nos permite trabajar con archivos y acceder a sus rutas etc.
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = 'database.sqlite'# Aqui damos nombre a el archivo de las BASE DE DATOS SQLITE (por eso la terminación '.sqlite')
base_dir = os.path.dirname(os.path.realpath(__file__)) # En esta parte la podemos subdividir.
# __FILE__ : Es una palabra reservada que hace referencia al archivo en el que se ejecuta
# OS.PATH.REALPATH(__FILE__) : Una funcipon que nos permite obtener la ruta absoluta del parametro que se le pase, em -> (/home/brynt/archivo.txt)
# OS.PATH.DIRNAME() : Una función que nos devuelve la ubicación del directorio del parametro que se le pase, bajo el mimso ejemplo anterior nos devolveria lo siguiente -> (/home/brynt).

#IMPORTANTE: La combinación de ambos nos permite evitar obtener una ruta equibocada en caso el código se este ejecutado en una dirección diferente a la caprte del proyecto, como por ejemplo un 'enlace simbolico' (Un archivo que hace referencia a otro archivo en una uvicación diferente)

database_url = f'sqlite:///{os.path.join(base_dir, sqlite_file_name)}' # Aqui concatenamos las partes constuidas anteriormente, el nombre del archivo que seria nuestra BD (Base de datos) y la ruta que obtuvimos.
# Esto creara una ruta final (URL) donde se encontrara nuestra BD
# 'sqlite:' Nos indica que se utilizara el tipo de base de datos SQLITE
# '///' Nos indica que es una ruta relativa, es decir que es en función a la ubicación del archivo en el que se ejecuta.
# Ejm -> si el archivo que se está ejecutando se encuentra en la carpeta "proyecto" y se desea acceder a un archivo llamado "datos.txt" en la subcarpeta "datos", la ruta relativa sería "datos/datos.txt". Si se utilizara una ruta absoluta, la ruta completa desde la raíz del sistema de archivos sería "/proyecto/datos/datos.txt".

engine = create_engine(database_url, echo=True) # Dividimos esta parte de la siguiente forma
# create_engine() : Es la función que crea el motor de base de datos y lo almacena en la ruta que guardamos en la bariable 'database_url'.
# El motor de base de datos no es un archivo, es mas bien un sofware que administra los datos de la base de datos SQLITE, al ejecutar esta linea de codigo se creara el archivo en la dirección que determinamos.
# echo=True : Esto permite que cuando hagamos consultas de SQL se muestre en la consola (La shell o el bash) mensajes de lo que se esta ejecutando en la base de datos
# OBS: estos mensajes osn predeterminados por SQLArchemy por tanto no tenemos que escribir ninuguna linea de código adicional y no lo determinamos nosotros.

session = sessionmaker(bind=engine) # Creamos un Manejador de sessiones
# SESSIONMAKER() : Resive como parametro el motor de base de datos y nos debuelbe una CLASE (class)
# Session : Es una clase creada a partir de 'sessionmaker()' y nos permite crear sesiones (objetos), que nos permitira hacer consultas eh interactuar con la base de dastos SQLITE

base = declarative_base() # Creamos una Clase 'base', esta clase nos sirve para poder crear de manera mas facil las tablas de nuestra BD, y tambien tiene las funcionalidades CRUD de la base de datos.
# Nos permite crear una tabla como crear un objeto en Python, siendo las caracteristicas las filas y columbas (Datos a llenar) y las funcionalidades seria el CRUD