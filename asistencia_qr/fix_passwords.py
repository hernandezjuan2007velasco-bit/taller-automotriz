import mysql.connector
from werkzeug.security import generate_password_hash
from config import Config
import certifi

new_hash = generate_password_hash('sena2026')
print('New hash:', new_hash)

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
cursor.execute('UPDATE usuarios SET password_hash = %s', (new_hash,))
conn.commit()
print('Passwords updated in TiDB successfully!')
conn.close()
