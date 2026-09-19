from config import Config

try:
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        port=Config.MYSQL_PORT,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        ssl={'ssl': True}
    )
    print('Success with pymysql!')
except Exception as e:
    print('PyMySQL Error:', e)
