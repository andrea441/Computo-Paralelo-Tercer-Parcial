import oracledb

# Función que ejecuta un script SQL o PL/SQL desde un archivo, línea por línea.
def run_script(cursor, filename):
    print(f"\nEjecutando: {filename}")
    # Abre el archivo y lee todas las líneas, las guarda en una lista llamada lines.
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    statement = '' # Acumula las líneas del script, para luego ejecutarlas.
    in_plsql_block = False # Indica si estamos dentro de un bloque PL/SQL.

    for line in lines:
        stripped = line.strip() # Elimina espacios al inicio y al final de la línea.

        # Si la línea está vacía o es un comentario, se ignora.
        if not stripped or stripped.startswith('--'):
            continue

        # Si la línea comienza con 'CREATE' y contiene 'TRIGGER', se considera que estamos en un bloque PL/SQL.
        # Esto es para manejar correctamente los bloques PL/SQL que terminan con '/'.
        if stripped.upper().startswith('CREATE') and 'TRIGGER' in stripped.upper():
            in_plsql_block = True

        # Se acumula la línea en la variable statement.
        statement += line

        # Si estamos en un bloque PL/SQL, se espera a que la línea termine con '/' para ejecutar el bloque.
        if in_plsql_block:
            if stripped == '/':
                try:
                    cursor.execute(statement.rsplit('/', 1)[0])
                except Exception as e:
                    print(f"Error en bloque PL/SQL:\n{statement}\n{e}")
                statement = ''
                in_plsql_block = False

        # Si no estamos en un bloque PL/SQL, se ejecuta la sentencia cuando termina con ';'.
        else:
            if stripped.endswith(';'):
                try:
                    cursor.execute(statement.rstrip().rstrip(';'))
                except Exception as e:
                    print(f"Error en sentencia SQL:\n{statement}\n{e}")
                statement = ''

# Función para conectar a una base de datos Oracle, dada una cadena de conexión (DSN) y un nombre descriptivo.
def conectar(dsn, nombre):
    try:
        # Intenta establecer la conexión a la base de datos Oracle usando el DSN proporcionado.
        conn = oracledb.connect(user="system", password="oracle", dsn=dsn)
        print(f"Conectado a {nombre}")
        return conn, conn.cursor()
    # Si ocurre un error al conectar, se captura la excepción y se imprime un mensaje de error.
    except Exception as e:
        print(f"Error al conectar a {nombre}: {e}")
        return None, None

def main():
    # Definición de las cadenas de conexión (DSN) para las bases de datos Oracle Nodo A y B.
    dsn1 = "localhost:1521/XEPDB1"
    dsn2 = "localhost:1522/XEPDB1"

    # Conexión a las bases de datos Oracle usando las cadenas de conexión definidas.
    conn1, cur1 = conectar(dsn1, "oracle1")
    conn2, cur2 = conectar(dsn2, "oracle2")

    # Si alguna de las conexiones falla, se termina la ejecución del script.
    if not conn1 or not conn2:
        return
    
    # Ejecuta el script inicial en ambas bases de datos.
    for cur, nombre in [(cur1, "Oracle1"), (cur2, "Oracle2")]:
        print(f"\nEjecutando script inicial en {nombre}")
        run_script(cur, 'sql-scripts/first.sql')
    
    # Commit de las transacciones para asegurar que los cambios se guarden en la base de datos.
    conn1.commit()
    conn2.commit()

    input("\nPresiona Enter para continuar con la inserción de datos...")

    # Ejecuta los scripts de inserción de datos en ambas bases de datos.
    run_script(cur1, 'sql-scripts/oracle1.sql')
    run_script(cur2, 'sql-scripts/oracle2.sql')

    # Commit de las transacciones nuevamente para guardar los cambios.
    conn1.commit()
    conn2.commit()

    print("\nTodos los scripts ejecutados correctamente.")

    # Cierra los cursores y las conexiones a las bases de datos.
    cur1.close()
    conn1.close()
    cur2.close()
    conn2.close()

if __name__ == '__main__':
    main()

