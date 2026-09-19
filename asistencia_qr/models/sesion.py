"""
Modelo de Sesión — Gestión de sesiones de clase con QR.
"""
from models.db import ejecutar_consulta, ejecutar_transaccion
from datetime import datetime, date


def crear(ficha_id, instructor_id, ip_instructor):
    """Crea una nueva sesión de asistencia con la IP del instructor."""
    query = """
        INSERT INTO sesiones (ficha_id, instructor_id, fecha, hora_inicio, ip_instructor, estado)
        VALUES (%s, %s, %s, %s, %s, 'activa')
    """
    hoy = date.today()
    ahora = datetime.now().strftime('%H:%M:%S')
    return ejecutar_consulta(query, (ficha_id, instructor_id, hoy, ahora, ip_instructor), commit=True)


def obtener_por_id(id):
    """Obtiene una sesión por su ID."""
    query = "SELECT * FROM sesiones WHERE id = %s"
    return ejecutar_consulta(query, (id,), fetchone=True)

def obtener_todas_por_instructor(instructor_id):
    """Obtiene todas las sesiones (activas y pasadas) de un instructor."""
    query = """
        SELECT s.*, f.numero as ficha_numero, f.programa as ficha_programa,
               (SELECT COUNT(*) FROM asistencias a WHERE a.sesion_id = s.id AND a.estado IN ('presente','corregido')) as asistencias_count
        FROM sesiones s
        JOIN fichas f ON s.ficha_id = f.id
        WHERE s.instructor_id = %s
        ORDER BY s.fecha DESC, s.hora_inicio DESC
    """
    return ejecutar_consulta(query, (instructor_id,), fetchall=True)




def obtener_activa_por_instructor(instructor_id):
    """Obtiene la sesión activa del instructor (solo puede tener una)."""
    query = """
        SELECT s.*, f.numero as ficha_numero, f.programa as ficha_programa
        FROM sesiones s
        JOIN fichas f ON s.ficha_id = f.id
        WHERE s.instructor_id = %s AND s.estado = 'activa'
    """
    return ejecutar_consulta(query, (instructor_id,), fetchone=True)


def cerrar(sesion_id):
    """Cierra una sesión de asistencia y marca ausentes a los faltantes de forma atómica."""
    ahora = datetime.now().strftime('%H:%M:%S')
    
    # 1. Insertar inasistencias automáticamente para los aprendices que no marcaron
    query_ausencias = """
        INSERT INTO asistencias (sesion_id, aprendiz_id, estado, hora_registro, ip_registro)
        SELECT %s, fa.aprendiz_id, 'ausente', %s, 'sistema'
        FROM ficha_aprendiz fa
        LEFT JOIN asistencias a ON a.sesion_id = %s AND a.aprendiz_id = fa.aprendiz_id
        WHERE fa.ficha_id = (SELECT ficha_id FROM sesiones WHERE id = %s)
        AND a.id IS NULL
    """
    
    # 2. Cerrar la sesión
    query_cierre = "UPDATE sesiones SET estado = 'cerrada', hora_fin = %s WHERE id = %s"
    
    consultas = [
        (query_ausencias, (sesion_id, ahora, sesion_id, sesion_id)),
        (query_cierre, (ahora, sesion_id))
    ]
    ejecutar_transaccion(consultas)
    return True


def actualizar_codigo(sesion_id, codigo):
    """Actualiza el código QR vigente de una sesión."""
    import time
    timestamp = int(time.time())
    query = "UPDATE sesiones SET codigo_actual = %s, codigo_timestamp = %s WHERE id = %s"
    ejecutar_consulta(query, (codigo, timestamp, sesion_id), commit=True)
    return True
