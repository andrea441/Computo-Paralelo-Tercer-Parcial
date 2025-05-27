import oracledb

def run_script(cursor, filename):
    print(f"\nEjecutando: {filename}")
    with open(filename, 'r') as f:
        lines = f.readlines()

    statement = ''
    in_plsql_block = False

    for line in lines:
        stripped = line.strip()

        if not stripped or stripped.startswith('--'):
            continue

        if stripped.upper().startswith('CREATE') and 'TRIGGER' in stripped.upper():
            in_plsql_block = True

        statement += line

        if in_plsql_block:
            if stripped == '/':
                try:
                    cursor.execute(statement.rsplit('/', 1)[0])
                except Exception as e:
                    print(f"Error en bloque PL/SQL:\n{statement}\n{e}")
                statement = ''
                in_plsql_block = False
        else:
            if stripped.endswith(';'):
                try:
                    cursor.execute(statement.rstrip().rstrip(';'))
                except Exception as e:
                    print(f"Error en sentencia SQL:\n{statement}\n{e}")
                statement = ''

def conectar(dsn, nombre):
    try:
        conn = oracledb.connect(user="system", password="oracle", dsn=dsn)
        print(f"Conectado a {nombre}")
        return conn, conn.cursor()
    except Exception as e:
        print(f"Error al conectar a {nombre}: {e}")
        return None, None

def main():
    dsn1 = "localhost:1521/XEPDB1"
    dsn2 = "localhost:1522/XEPDB1"

    conn1, cur1 = conectar(dsn1, "oracle1")
    conn2, cur2 = conectar(dsn2, "oracle2")

    if not conn1 or not conn2:
        return

    for cur, nombre in [(cur1, "Oracle1"), (cur2, "Oracle2")]:
        print(f"\nEjecutando script inicial en {nombre}")
        run_script(cur, 'sql-scripts/first.sql')

    conn1.commit()
    conn2.commit()

    input("\nPresiona Enter para continuar con la inserción de datos...")

    run_script(cur1, 'sql-scripts/oracle1.sql')
    run_script(cur2, 'sql-scripts/oracle2.sql')

    conn1.commit()
    conn2.commit()

    print("\nTodos los scripts ejecutados correctamente.")

    cur1.close()
    conn1.close()
    cur2.close()
    conn2.close()

if __name__ == '__main__':
    main()

