from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Creación del consumidor de Kafka. Se conecta al servidor Kafka levantado en docker-compose.
# Escucha mensajes del topic "replicacion_banco".
consumer = KafkaConsumer(
    'replicacion_banco',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Se establece la conexión a MongoDB, desde el contenedor mongo levantado en docker-compose.
mongo = MongoClient("mongodb://mongo:27017/")
db = mongo["banco"] # Accede o crea la base de datos "banco".
col_sucursal = db["sucursal"] # Accede o crea la colección "sucursal".
col_prestamo = db["prestamo"] # Accede o crea la colección "prestamo".

# Bucle infinito que espera recibir mensajes del topic "replicacion_banco".
for msg in consumer: # Por cada mensaje recibido:
    contenido = msg.value
    tabla = contenido['tabla'] # Se obtiene la tabla afectada, puede ser "sucursal" o "prestamo".
    operacion = contenido['operacion'] # Se obtiene la operación realizada, puede ser "insert", "delete" o "update".
    datos = contenido['datos'] # Se obtienen los datos del mensaje, que son un diccionario de Python.

    # Dependiendo de la tabla, se selecciona la colección y el filtro (id) adecuado.
    if tabla == "sucursal":
        col = col_sucursal
        filtro = {"idsucursal": datos["idsucursal"]}
    elif tabla == "prestamo":
        col = col_prestamo
        filtro = {"noprestamo": datos["noprestamo"]}
    else:
        continue

    # Dependiendo de la operación, se realiza la acción correspondiente en MongoDB.
    if operacion == "insert":
        col.insert_one(datos)
    elif operacion == "delete":
        col.delete_one(filtro)
    elif operacion == "update":
        col.update_one(filtro, {"$set": datos})
