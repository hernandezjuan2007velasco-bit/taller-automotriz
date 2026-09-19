import mysql.connector
from config import Config

import certifi

def init_db():
    print("Connecting to TiDB Cloud...")
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            ssl_verify_cert=True,
            ssl_verify_identity=True,
            ssl_ca=certifi.where()
        )
        cursor = conn.cursor()
        
        print("Creating database asistencia_qr if not exists...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS asistencia_qr;")
        cursor.execute("USE asistencia_qr;")
        
        print("Executing schema.sql...")
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            
        for result in cursor.execute(schema_sql, multi=True):
            pass # Exhaust the generator to execute all statements
                
        print("Executing seeds.sql...")
        with open('database/seeds.sql', 'r', encoding='utf-8') as f:
            seeds_sql = f.read()
            
        for result in cursor.execute(seeds_sql, multi=True):
            pass # Exhaust the generator
                
        conn.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print("Error during initialization:", e)
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    init_db()
