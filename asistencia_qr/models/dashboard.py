from models.db import ejecutar_consulta

def obtener_metricas_admin():
    """Obtiene métricas globales para el dashboard del administrador."""
    
    # Usuarios
    totales_usuarios = ejecutar_consulta("SELECT rol, COUNT(*) as count FROM usuarios GROUP BY rol", fetchall=True)
    total_aprendices = 0
    total_instructores = 0
    for u in totales_usuarios:
        if u['rol'] == 'aprendiz':
            total_aprendices = u['count']
        elif u['rol'] == 'instructor':
            total_instructores = u['count']
            
    # Fichas
    total_fichas = ejecutar_consulta("SELECT COUNT(*) as count FROM fichas WHERE estado = 'activa'", fetchone=True)['count']
    
    # Sesiones activas (QR activos)
    sesiones_activas = ejecutar_consulta("SELECT COUNT(*) as count FROM sesiones WHERE estado = 'activa'", fetchone=True)['count']
    
    # Asistencias y Ausencias HOY
    asistencias_hoy = ejecutar_consulta("""
        SELECT a.estado, COUNT(*) as count 
        FROM asistencias a
        JOIN sesiones s ON a.sesion_id = s.id
        WHERE s.fecha = CURRENT_DATE
        GROUP BY a.estado
    """, fetchall=True)
    
    total_presentes = 0
    total_ausentes = 0
    for a in asistencias_hoy:
        if a['estado'] == 'presente':
            total_presentes = a['count']
        elif a['estado'] == 'ausente':
            total_ausentes = a['count']
            
    # Alertas activas
    alertas_activas = ejecutar_consulta("SELECT COUNT(*) as count FROM alertas WHERE estado = 'activa'", fetchone=True)['count']
    
    return {
        'total_aprendices': total_aprendices,
        'total_instructores': total_instructores,
        'fichas_activas': total_fichas,
        'sesiones_activas': sesiones_activas,
        'asistencias_hoy': total_presentes,
        'ausencias_hoy': total_ausentes,
        'alertas_activas': alertas_activas
    }

def obtener_metricas_instructor(instructor_id):
    """Obtiene métricas para el dashboard del instructor."""
    # Fichas asignadas
    total_fichas = ejecutar_consulta("SELECT COUNT(*) as count FROM fichas WHERE instructor_id = %s", (instructor_id,), fetchone=True)['count']
    
    # Sesiones totales realizadas
    total_sesiones = ejecutar_consulta("SELECT COUNT(*) as count FROM sesiones WHERE instructor_id = %s", (instructor_id,), fetchone=True)['count']
    
    # Promedio de asistencia global (aproximado)
    # Total de asistencias registradas / Total de aprendices esperados en esas sesiones
    # Por simplicidad: Asistencias totales vs Ausencias totales
    asistencias = ejecutar_consulta("""
        SELECT a.estado, COUNT(*) as count 
        FROM asistencias a
        JOIN sesiones s ON a.sesion_id = s.id
        WHERE s.instructor_id = %s
        GROUP BY a.estado
    """, (instructor_id,), fetchall=True)
    
    presentes = 0
    ausentes = 0
    for a in asistencias:
        if a['estado'] == 'presente' or a['estado'] == 'corregido':
            presentes += a['count']
        elif a['estado'] == 'ausente':
            ausentes += a['count']
            
    total_registros = presentes + ausentes
    asistencia_promedio = round((presentes / total_registros * 100) if total_registros > 0 else 0, 1)
    
    # Sesiones activas actualmente
    sesiones_activas = ejecutar_consulta("SELECT COUNT(*) as count FROM sesiones WHERE instructor_id = %s AND estado = 'activa'", (instructor_id,), fetchone=True)['count']
    
    return {
        'total_fichas': total_fichas,
        'total_sesiones': total_sesiones,
        'asistencia_promedio': asistencia_promedio,
        'sesiones_activas': sesiones_activas
    }
