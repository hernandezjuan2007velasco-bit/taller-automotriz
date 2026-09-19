"""
Script de verificación de conexión a la base de datos TiDB Cloud / MySQL.
"""
from models.db import obtener_conexion

def test_conexion():
    print("Probando conexión a la base de datos...")
    try:
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DATABASE() as db, VERSION() as version, NOW() as hora;")
        res = cursor.fetchone()
        print(" Conexión exitosa:")
        print(f"  Base de datos: {res['db']}")
        print(f"  Versión:       {res['version']}")
        print(f"  Hora servidor: {res['hora']}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(" Error al conectar con la base de datos:")
        print(f"  Detalle: {e}")
        return False

if __name__ == '__main__':
    test_conexion()

