import mysql.connector
import certifi

from config import Config

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
cursor = conn.cursor(dictionary=True)
cursor.execute('SELECT documento, password_hash, rol, estado FROM usuarios LIMIT 5;')
for row in cursor:
    print(row)
conn.close()
