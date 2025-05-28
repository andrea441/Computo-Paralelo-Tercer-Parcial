from kafka import KafkaProducer
import oracledb
import json
import time
import threading
import logging

# Configuración del logging, para los mensajes de log en la consola.
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(threadName)s] %(message)s',
    datefmt='%H:%M:%S'
)

# Función para conectarse a una base de datos Oracle.
def conectar_oracle(user, password, dsn):
    return oracledb.connect(user=user, password=password, dsn=dsn)

# Creación de dos conexiones a bases de datos Oracle, usando la función anterior.
conn1 = conectar_oracle("system", "oracle", "oracle1:1521/XEPDB1") # Región A
conn2 = conectar_oracle("system", "oracle", "oracle2:1521/XEPDB1") # Región B

# Creación del productor de Kafka. Se conecta al servidor Kafka levantado en docker-compose.
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Función que se ejecuta en un hilo para leer eventos de replicación desde la base de datos y enviarlos a Kafka.
# Es un bucle infinito, lee los eventos de la tabla `log_replicacion` cada 5 segundos.
def producir_desde_base(nombre_origen, conn):
    cur = conn.cursor()
    while True:
        cur.execute("SELECT rowid, tabla, operacion, datos FROM log_replicacion")
        rows = cur.fetchall()

        if rows:
            logging.info(f"{len(rows)} eventos encontrados en {nombre_origen}")

        # Se recorren las filas obtenidas de la consulta.    
        for row in rows:
            rowid, tabla, operacion, datos = row
            try:
                json_datos = json.loads(datos.read() if hasattr(datos, 'read') else datos) # Se convierten los datos a un diccionario de Python.
                
                # Se construye un mensaje con el origen, la tabla, la operación y los datos
                msg = {
                    "origen": nombre_origen,
                    "tabla": tabla,
                    "operacion": operacion,
                    "datos": json_datos
                }

                producer.send("replicacion_banco", msg) # Se envía al topic "replicacion_banco" de Kafka.
                logging.info(f"{operacion.upper()} en {tabla} replicado desde {nombre_origen}: {json_datos}")

                # Después de procesar un cambio, se borra de la tabla log_replicacion.
                cur.execute("DELETE FROM log_replicacion WHERE rowid = :1", [rowid])
                conn.commit()

            except Exception as e:
                logging.error(f"Error procesando fila desde {nombre_origen}: {e}")

        time.sleep(5)

# Esto crea dos hilos de ejecución en paralelo, uno por base de datos.
hilo1 = threading.Thread(target=producir_desde_base, args=("Oracle_A", conn1), name="Oracle_A")
hilo2 = threading.Thread(target=producir_desde_base, args=("Oracle_B", conn2), name="Oracle_B")

# Se arrancan los dos hilos.
hilo1.start()
hilo2.start()

# Se espera a que terminen los hilos, lo cual nunca ocurre, porque el bucle es infinito,
hilo1.join()
hilo2.join()
