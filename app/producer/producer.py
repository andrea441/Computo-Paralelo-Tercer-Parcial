from kafka import KafkaProducer
import oracledb
import json
import time
import threading
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(threadName)s] %(message)s',
    datefmt='%H:%M:%S'
)

def conectar_oracle(user, password, dsn):
    return oracledb.connect(user=user, password=password, dsn=dsn)

conn1 = conectar_oracle("system", "oracle", "oracle1:1521/XEPDB1")
conn2 = conectar_oracle("system", "oracle", "oracle2:1521/XEPDB1")

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def producir_desde_base(nombre_origen, conn):
    cur = conn.cursor()
    while True:
        cur.execute("SELECT rowid, tabla, operacion, datos FROM log_replicacion")
        rows = cur.fetchall()

        if rows:
            logging.info(f"{len(rows)} eventos encontrados en {nombre_origen}")

        for row in rows:
            rowid, tabla, operacion, datos = row
            try:
                json_datos = json.loads(datos.read() if hasattr(datos, 'read') else datos)

                msg = {
                    "origen": nombre_origen,
                    "tabla": tabla,
                    "operacion": operacion,
                    "datos": json_datos
                }

                producer.send("replicacion_banco", msg)
                logging.info(f"{operacion.upper()} en {tabla} replicado desde {nombre_origen}: {json_datos}")

                cur.execute("DELETE FROM log_replicacion WHERE rowid = :1", [rowid])
                conn.commit()

            except Exception as e:
                logging.error(f"Error procesando fila desde {nombre_origen}: {e}")

        time.sleep(5)

hilo1 = threading.Thread(target=producir_desde_base, args=("Oracle_A", conn1), name="Oracle_A")
hilo2 = threading.Thread(target=producir_desde_base, args=("Oracle_B", conn2), name="Oracle_B")

hilo1.start()
hilo2.start()

hilo1.join()
hilo2.join()
