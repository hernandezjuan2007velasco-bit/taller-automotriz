import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env si existe (entorno local)
load_dotenv()

class Config:
    """Configuración general de la aplicación."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-asistencia-qr-sena-2026')
    
    # Base de datos MySQL / TiDB Cloud
    MYSQL_HOST = os.environ.get('MYSQL_HOST')
    MYSQL_USER = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB = os.environ.get('MYSQL_DB')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 4000))
    
    # Modo de depuración (útil para el manejo de errores)
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    
    # Seguridad y Sesiones
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Seguridad QR
    QR_HMAC_SECRET = os.environ.get('QR_HMAC_SECRET', 'hmac-secreto-qr-sena-antifraude-2026')
    QR_ROTACION_SEGUNDOS = 30       # El QR cambia cada 30 segundos
    QR_TOLERANCIA_PERIODOS = 1      # Acepta 1 período anterior (ventana efectiva ~60s)
    
    # Validación de red (False por defecto para permitir que funcione con datos móviles, Wi-Fi o enlaces públicos)
    VALIDAR_RED = os.environ.get('VALIDAR_RED', 'False').lower() in ['true', '1', 't']
    MASCARA_SUBRED = int(os.environ.get('MASCARA_SUBRED', 24))
