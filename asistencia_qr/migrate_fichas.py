import mysql.connector
import certifi
from config import Config

def migrate():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            ssl_verify_cert=True,
            ssl_verify_identity=True,
            ssl_ca=certifi.where()
        )
        cursor = conn.cursor()
        
        # Add estado
        try:
            cursor.execute("ALTER TABLE fichas ADD COLUMN estado ENUM('activa', 'suspendida', 'finalizada', 'archivada') DEFAULT 'activa'")
            print("Columna 'estado' añadida.")
        except mysql.connector.Error as err:
            print(f"Nota (estado): {err.msg}")
            
        # Add fecha_apertura
        try:
            cursor.execute("ALTER TABLE fichas ADD COLUMN fecha_apertura DATE")
            print("Columna 'fecha_apertura' añadida.")
        except mysql.connector.Error as err:
            print(f"Nota (fecha_apertura): {err.msg}")
            
        # Add fecha_cierre
        try:
            cursor.execute("ALTER TABLE fichas ADD COLUMN fecha_cierre DATE")
            print("Columna 'fecha_cierre' añadida.")
        except mysql.connector.Error as err:
            print(f"Nota (fecha_cierre): {err.msg}")
            
        conn.commit()
        print("Migración completada con éxito.")
    except Exception as e:
        print(f"Error fatal: {str(e)}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == '__main__':
    # Simular carga de dotenv para acceso a os.environ
    from dotenv import load_dotenv
    load_dotenv()
    migrate()
