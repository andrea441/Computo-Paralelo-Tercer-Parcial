from kafka import KafkaConsumer
from pymongo import MongoClient
import json

consumer = KafkaConsumer(
    'replicacion_banco',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

mongo = MongoClient("mongodb://mongo:27017/")
db = mongo["banco"]
col_sucursal = db["sucursal"]
col_prestamo = db["prestamo"]

for msg in consumer:
    contenido = msg.value
    tabla = contenido['tabla']
    operacion = contenido['operacion']
    datos = contenido['datos']

    if tabla == "sucursal":
        col = col_sucursal
        filtro = {"idsucursal": datos["idsucursal"]}
    elif tabla == "prestamo":
        col = col_prestamo
        filtro = {"noprestamo": datos["noprestamo"]}
    else:
        continue

    if operacion == "insert":
        col.insert_one(datos)
    elif operacion == "delete":
        col.delete_one(filtro)
    elif operacion == "update":
        col.update_one(filtro, {"$set": datos})
