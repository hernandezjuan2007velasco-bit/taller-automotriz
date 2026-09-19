"""
Módulo de seguridad y anti-fraude.
Contiene las funciones centrales para: HMAC, validación de red, anti-duplicado, auditoría.
"""

import hmac
import hashlib
import time
from ipaddress import ip_address, ip_network


def generar_codigo_qr(sesion_id, secreto):
    """
    Genera un código QR firmado con HMAC.
    El código cambia cada 30 segundos (configurable).
    
    Formato: {sesion_id}-{periodo}-{firma_hmac_8chars}
    """
    periodo = int(time.time()) // 30  # Cambia cada 30 segundos
    mensaje = f"{sesion_id}-{periodo}"
    firma = hmac.new(
        secreto.encode(), 
        mensaje.encode(), 
        hashlib.sha256
    ).hexdigest()[:8].upper()
    return f"{sesion_id}-{periodo}-{firma}"


def verificar_codigo_qr(codigo_recibido, secreto, tolerancia=1):
    """
    Verifica que un código QR sea válido:
    1. Que la firma HMAC coincida (no fue fabricado)
    2. Que no haya expirado (dentro de la ventana de tolerancia)
    
    Retorna el sesion_id si es válido, None si no.
    """
    try:
        codigo_limpio = str(codigo_recibido or '').strip()
        partes = codigo_limpio.split("-")
        if len(partes) != 3:
            return None
        
        sesion_id = int(partes[0].strip())
        periodo_recibido = int(partes[1].strip())
        firma_recibida = partes[2].strip().upper()
        
        # Verificar que no esté expirado
        periodo_actual = int(time.time()) // 30
        if abs(periodo_actual - periodo_recibido) > tolerancia:
            return None
        
        # Verificar firma HMAC
        mensaje = f"{sesion_id}-{periodo_recibido}"
        firma_esperada = hmac.new(
            secreto.encode(), 
            mensaje.encode(), 
            hashlib.sha256
        ).hexdigest()[:8].upper()
        
        if hmac.compare_digest(firma_recibida, firma_esperada):
            return sesion_id
        return None
    except (ValueError, IndexError, AttributeError):
        return None


def misma_subred(ip_instructor, ip_aprendiz, mascara=24):
    """
    Verifica que el aprendiz esté en la misma subred que el instructor.
    Ejemplo: si el instructor tiene 10.42.15.100 y la máscara es /24,
    el aprendiz debe tener una IP en 10.42.15.0/24.
    
    Retorna True si están en la misma subred.
    """
    try:
        red_instructor = ip_network(f"{ip_instructor}/{mascara}", strict=False)
        return ip_address(ip_aprendiz) in red_instructor
    except (ValueError, TypeError):
        return False


def obtener_ip_real(request):
    """
    Obtiene la IP real del cliente, considerando proxies.
    """
    # Si hay un proxy inverso (nginx, etc.), la IP real viene en X-Forwarded-For
    if request.headers.get('X-Forwarded-For'):
        return request.headers['X-Forwarded-For'].split(',')[0].strip()
    if request.headers.get('X-Real-Ip'):
        return request.headers['X-Real-Ip']
    return request.remote_addr


def hash_password(password):
    """Genera hash seguro de contraseña usando SHA-256 con salt."""
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)


def verificar_password(password_hash, password):
    """Verifica una contraseña contra su hash."""
    from werkzeug.security import check_password_hash
    return check_password_hash(password_hash, password)
