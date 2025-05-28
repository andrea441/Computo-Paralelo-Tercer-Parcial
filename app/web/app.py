from flask import Flask, render_template, request, redirect
import oracledb

# Se inicializa la aplicación Flask.
app = Flask(__name__)

# Se crea la conexión a la base de datos Oracle, específicamente el nodo de la región A.
conn = oracledb.connect(
    user="system",
    password="oracle",
    dsn="oracle1:1521/XEPDB1"
)

# Ruta principal que renderiza la página de inicio.
@app.route('/')
def index():
    # Se crea un cursor para ejecutar consultas SQL.
    cur = conn.cursor()

    # Obtener todas las sucursales.
    cur.execute("SELECT * FROM sucursal")
    sucursales = cur.fetchall()

    # Obtener todos los préstamos.
    cur.execute("SELECT * FROM prestamo")
    prestamos = cur.fetchall()

    # Obtener totales y sumas para mostrar en la página.
    cur.execute("SELECT COUNT(*) FROM sucursal")
    total_sucursales = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM prestamo")
    total_prestamos = cur.fetchone()[0]

    cur.execute("SELECT SUM(activos) FROM sucursal")
    activos_totales = cur.fetchone()[0]

    return render_template(
        "index.html",
        sucursales=sucursales,
        prestamos=prestamos,
        total_sucursales=total_sucursales,
        total_prestamos=total_prestamos,
        activos_totales=activos_totales
    )

# Rutas para insertar y eliminar sucursales y préstamos.
@app.route('/insert_sucursal', methods=['POST'])
def insert_sucursal():
    data = (
        request.form['idsucursal'],
        request.form['nombresucursal'],
        request.form['ciudadsucursal'],
        request.form['activos'],
        request.form['region']
    )

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sucursal (idsucursal, nombresucursal, ciudadsucursal, activos, region)
        VALUES (:1, :2, :3, :4, :5)
    """, data)
    conn.commit()
    return redirect('/')

@app.route('/insert_prestamo', methods=['POST'])
def insert_prestamo():
    data = (
        request.form['noprestamo'],
        request.form['idsucursal'],
        request.form['cantidad']
    )

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO prestamo (noprestamo, idsucursal, cantidad)
        VALUES (:1, :2, :3)
    """, data)
    conn.commit()
    return redirect('/')

@app.route('/delete_sucursal', methods=['POST'])
def delete_sucursal():
    idsucursal = request.form['idsucursal']
    cur = conn.cursor()
    cur.execute("DELETE FROM sucursal WHERE idsucursal = :1", [idsucursal])
    conn.commit()
    return redirect('/')

@app.route('/delete_prestamo', methods=['POST'])
def delete_prestamo():
    noprestamo = request.form['noprestamo']
    cur = conn.cursor()
    cur.execute("DELETE FROM prestamo WHERE noprestamo = :1", [noprestamo])
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
