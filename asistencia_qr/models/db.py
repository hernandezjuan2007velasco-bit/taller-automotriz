"""
Módulo de conexión a la base de datos MySQL.
Proporciona funciones para obtener conexión y ejecutar consultas con pool de conexiones.
"""

import mysql.connector
from mysql.connector import pooling
from config import Config
import certifi
import logging

logger = logging.getLogger(__name__)


class DatabaseConnectionError(Exception):
    """Excepción personalizada para errores de conexión a la base de datos."""
    pass


_connection_pool = None


def _crear_pool():
    """Inicializa el pool de conexiones si no existe."""
    global _connection_pool
    if _connection_pool is not None:
        return _connection_pool

    if not all([Config.MYSQL_HOST, Config.MYSQL_USER, Config.MYSQL_PASSWORD, Config.MYSQL_DB]):
        raise DatabaseConnectionError("Faltan variables de entorno para la conexión a la base de datos.")

    kwargs = {
        'host': Config.MYSQL_HOST,
        'user': Config.MYSQL_USER,
        'password': Config.MYSQL_PASSWORD,
        'database': Config.MYSQL_DB,
        'port': Config.MYSQL_PORT
    }

    if 'tidbcloud.com' in Config.MYSQL_HOST:
        kwargs['ssl_verify_cert'] = True
        kwargs['ssl_verify_identity'] = True
        kwargs['ssl_ca'] = certifi.where()

    try:
        _connection_pool = pooling.MySQLConnectionPool(
            pool_name="asistencia_pool",
            pool_size=5,
            pool_reset_session=True,
            **kwargs
        )
        return _connection_pool
    except Exception as e:
        logger.warning(f"No se pudo crear el pool de conexiones: {e}. Se utilizarán conexiones directas.")
        return None


def obtener_conexion():
    """Crea y retorna una conexión a la base de datos MySQL (desde el pool o directa)."""
    global _connection_pool
    if _connection_pool is None:
        _crear_pool()

    conn = None
    if _connection_pool:
        try:
            conn = _connection_pool.get_connection()
        except Exception:
            conn = None

    if conn is None:
        if not all([Config.MYSQL_HOST, Config.MYSQL_USER, Config.MYSQL_PASSWORD, Config.MYSQL_DB]):
            raise DatabaseConnectionError("Faltan variables de entorno para la conexión a la base de datos.")

        kwargs = {
            'host': Config.MYSQL_HOST,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DB,
            'port': Config.MYSQL_PORT
        }

        if 'tidbcloud.com' in Config.MYSQL_HOST:
            kwargs['ssl_verify_cert'] = True
            kwargs['ssl_verify_identity'] = True
            kwargs['ssl_ca'] = certifi.where()

        try:
            conn = mysql.connector.connect(**kwargs)
        except mysql.connector.Error as err:
            error_msg = f"Error conectando a la BD. Código: {err.errno}. Detalle: {err.msg}"
            raise DatabaseConnectionError(error_msg) from err

    try:
        cursor = conn.cursor()
        cursor.execute("SET time_zone = '-05:00'")
        cursor.close()
    except Exception:
        pass

    return conn


def ejecutar_consulta(query, params=None, fetchone=False, fetchall=False, commit=False):
    """
    Ejecuta una consulta SQL y retorna el resultado.
    """
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        
        if commit:
            conn.commit()
            return cursor.lastrowid
        
        if fetchone:
            return cursor.fetchone()
        
        if fetchall:
            return cursor.fetchall()
        
        return None
    except mysql.connector.IntegrityError as e:
        conn.rollback()
        raise e
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def ejecutar_transaccion(consultas):
    """
    Ejecuta múltiples consultas SQL dentro de una sola transacción atómica.
    Args:
        consultas: Lista de tuplas (query, params)
    Returns:
        True si todas las consultas se ejecutaron y committearon con éxito.
    """
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    try:
        for query, params in consultas:
            cursor.execute(query, params or ())
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()
