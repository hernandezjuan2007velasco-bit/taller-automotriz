"""
Modelo de Asistencia — Registros de asistencia con medidas anti-fraude.
"""
from models.db import ejecutar_consulta
from datetime import datetime


def registrar(sesion_id, aprendiz_id, ip_registro=None):
    """
    Registra la asistencia de un aprendiz.
    La restricción UNIQUE(sesion_id, aprendiz_id) previene duplicados.
    """
    hora = datetime.now().strftime('%H:%M:%S')
    query = """
        INSERT INTO asistencias (sesion_id, aprendiz_id, hora_registro, ip_registro, estado)
        VALUES (%s, %s, %s, %s, 'presente')
    """
    return ejecutar_consulta(query, (sesion_id, aprendiz_id, hora, ip_registro), commit=True)


def obtener_por_sesion(sesion_id):
    """Obtiene todos los registros de asistencia de una sesión con datos del aprendiz."""
    query = """
        SELECT a.*, u.nombre, u.documento
        FROM asistencias a
        JOIN usuarios u ON a.aprendiz_id = u.id
        WHERE a.sesion_id = %s
        ORDER BY a.hora_registro ASC
    """
    registros = ejecutar_consulta(query, (sesion_id,), fetchall=True)
    
    # Formatear para la API JSON
    resultado = []
    for r in (registros or []):
        nombre = r['nombre']
        partes = nombre.split()
        iniciales = ''.join([p[0] for p in partes[:2]]).upper()
        hora = str(r['hora_registro']) if r['hora_registro'] else '--:--'
        # Convertir timedelta a string si es necesario
        if hasattr(r['hora_registro'], 'total_seconds'):
            total_s = int(r['hora_registro'].total_seconds())
            h, m = divmod(total_s, 3600)
            m, s = divmod(m, 60)
            hora = f"{h}:{m:02d} {'am' if h < 12 else 'pm'}"
        
        resultado.append({
            'nombre': nombre,
            'documento': r['documento'],
            'iniciales': iniciales,
            'hora': hora,
            'estado': r['estado']
        })
    
    return {'registros': resultado, 'total_aprendices': len(resultado)}


def contar_por_sesion(sesion_id):
    """Cuenta los registros de asistencia de una sesión."""
    query = "SELECT COUNT(*) as total FROM asistencias WHERE sesion_id = %s"
    resultado = ejecutar_consulta(query, (sesion_id,), fetchone=True)
    return resultado['total'] if resultado else 0


def ya_registro(sesion_id, aprendiz_id):
    """Verifica si un aprendiz ya registró asistencia en una sesión (anti-fraude)."""
    query = "SELECT 1 FROM asistencias WHERE sesion_id = %s AND aprendiz_id = %s"
    resultado = ejecutar_consulta(query, (sesion_id, aprendiz_id), fetchone=True)
    return resultado is not None


def obtener_historial(instructor_id=None, ficha_id=None, fecha_inicio=None, fecha_fin=None, estado=None, busqueda=None, pagina=1, por_pagina=15):
    """
    Obtiene el historial de asistencia filtrado con paginación y formato completo.
    Garantiza que ningún registro se pierda y soporta visualización por ficha o instructor.
    """
    condiciones = []
    params = []
    
    # Alcance de instructor / ficha
    if instructor_id:
        if ficha_id:
            condiciones.append("s.ficha_id = %s")
            params.append(ficha_id)
        else:
            condiciones.append("(s.instructor_id = %s OR f.instructor_id = %s)")
            params.extend([instructor_id, instructor_id])
    elif ficha_id:
        condiciones.append("s.ficha_id = %s")
        params.append(ficha_id)

    if fecha_inicio:
        condiciones.append("s.fecha >= %s")
        params.append(fecha_inicio)
    if fecha_fin:
        condiciones.append("s.fecha <= %s")
        params.append(fecha_fin)
    if estado:
        condiciones.append("a.estado = %s")
        params.append(estado)
    if busqueda:
        condiciones.append("(u.nombre LIKE %s OR u.documento LIKE %s)")
        busqueda_param = f"%{busqueda}%"
        params.extend([busqueda_param, busqueda_param])

    where_clause = "WHERE " + " AND ".join(condiciones) if condiciones else ""

    query_base = f"""
        FROM asistencias a
        JOIN sesiones s ON a.sesion_id = s.id
        JOIN usuarios u ON a.aprendiz_id = u.id
        JOIN fichas f ON s.ficha_id = f.id
        {where_clause}
    """
    
    query_count = f"SELECT COUNT(*) as total {query_base}"
    total_res = ejecutar_consulta(query_count, tuple(params), fetchone=True)
    total = total_res['total'] if total_res else 0
    
    query_data = f"""
        SELECT a.*, s.fecha, s.hora_inicio as sesion_hora_inicio, s.hora_fin as sesion_hora_fin,
               u.nombre, u.documento, f.numero as ficha_numero, f.programa as ficha_programa, f.programa as programa
        {query_base}
        ORDER BY s.fecha DESC, a.hora_registro DESC, a.id DESC
        LIMIT %s OFFSET %s
    """
    offset = (pagina - 1) * por_pagina
    params_data = list(params) + [por_pagina, offset]
    
    registros = ejecutar_consulta(query_data, tuple(params_data), fetchall=True) or []
    
    # Formateo defensivo para la vista e informes
    for r in registros:
        r['programa'] = r.get('ficha_programa') or r.get('programa') or ''
        nombre = r.get('nombre', '') or ''
        partes = nombre.split()
        r['iniciales'] = ''.join([p[0] for p in partes[:2]]).upper() if partes else 'AP'
        
        # Formato amigable de hora
        hr = r.get('hora_registro')
        if hasattr(hr, 'total_seconds'):
            total_s = int(hr.total_seconds())
            h, m = divmod(total_s, 3600)
            m, s = divmod(m, 60)
            ampm = 'am' if h < 12 else 'pm'
            h12 = h if (1 <= h <= 12) else (h - 12 if h > 12 else 12)
            r['hora_formateada'] = f"{h12:02d}:{m:02d} {ampm}"
        elif hr:
            r['hora_formateada'] = str(hr)
        else:
            r['hora_formateada'] = '—'
            
        # Formato de fecha
        fec = r.get('fecha')
        if hasattr(fec, 'strftime'):
            r['fecha_formateada'] = fec.strftime('%d/%m/%Y')
        elif fec:
            r['fecha_formateada'] = str(fec)
        else:
            r['fecha_formateada'] = '—'
            
    return {'registros': registros, 'total': total}


def corregir(asistencia_id, nuevo_estado, motivo=None):
    """Corrige manualmente el estado de asistencia de un aprendiz."""
    query = "UPDATE asistencias SET estado = %s, motivo_correccion = %s WHERE id = %s"
    ejecutar_consulta(query, (nuevo_estado, motivo, asistencia_id), commit=True)
    return True


def calcular_metricas(instructor_id=None, ficha_id=None, fecha_inicio=None, fecha_fin=None):
    """Calcula las métricas consolidadas de asistencia."""
    condiciones = []
    params = []
    
    if instructor_id:
        if ficha_id:
            condiciones.append("s.ficha_id = %s")
            params.append(ficha_id)
        else:
            condiciones.append("(s.instructor_id = %s OR f.instructor_id = %s)")
            params.extend([instructor_id, instructor_id])
    elif ficha_id:
        condiciones.append("s.ficha_id = %s")
        params.append(ficha_id)
        
    if fecha_inicio:
        condiciones.append("s.fecha >= %s")
        params.append(fecha_inicio)
    if fecha_fin:
        condiciones.append("s.fecha <= %s")
        params.append(fecha_fin)
        
    where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""
    
    # Total de sesiones únicas
    query_sesiones = f"SELECT COUNT(DISTINCT s.id) as total FROM sesiones s JOIN fichas f ON s.ficha_id = f.id {where}"
    ses_res = ejecutar_consulta(query_sesiones, tuple(params), fetchone=True)
    sesiones_total = ses_res['total'] if ses_res else 0
    
    # Asistentes (presente o corregido)
    and_or_where = "AND" if where else "WHERE"
    query_asistentes = f"""
        SELECT COUNT(a.id) as total 
        FROM asistencias a
        JOIN sesiones s ON a.sesion_id = s.id
        JOIN fichas f ON s.ficha_id = f.id
        {where} {and_or_where} a.estado IN ('presente', 'corregido')
    """
    asist_res = ejecutar_consulta(query_asistentes, tuple(params), fetchone=True)
    asistentes = asist_res['total'] if asist_res else 0
    
    # Inasistentes (ausentes)
    query_inasistentes = f"""
        SELECT COUNT(a.id) as total 
        FROM asistencias a
        JOIN sesiones s ON a.sesion_id = s.id
        JOIN fichas f ON s.ficha_id = f.id
        {where} {and_or_where} a.estado = 'ausente'
    """
    inasist_res = ejecutar_consulta(query_inasistentes, tuple(params), fetchone=True)
    inasistentes = inasist_res['total'] if inasist_res else 0
    
    # Porcentaje de asistencia
    total_registros = asistentes + inasistentes
    porcentaje = round((asistentes / total_registros * 100), 1) if total_registros > 0 else 0
    
    return {
        'sesiones_total': sesiones_total,
        'asistentes': asistentes,
        'inasistentes': inasistentes,
        'porcentaje': porcentaje
    }


def obtener_historial_aprendiz(aprendiz_id):
    """Obtiene el historial completo de un aprendiz formateado."""
    query = """
        SELECT a.*, s.fecha, s.hora_inicio as sesion_hora_inicio, 
               f.numero as ficha_numero, f.programa as ficha_programa, 
               u.nombre as instructor_nombre
        FROM asistencias a
        JOIN sesiones s ON a.sesion_id = s.id
        JOIN fichas f ON s.ficha_id = f.id
        JOIN usuarios u ON s.instructor_id = u.id
        WHERE a.aprendiz_id = %s
        ORDER BY s.fecha DESC, a.hora_registro DESC, a.id DESC
    """
    registros = ejecutar_consulta(query, (aprendiz_id,), fetchall=True) or []
    for r in registros:
        hr = r.get('hora_registro')
        if hasattr(hr, 'total_seconds'):
            total_s = int(hr.total_seconds())
            h, m = divmod(total_s, 3600)
            m, s = divmod(m, 60)
            ampm = 'am' if h < 12 else 'pm'
            h12 = h if (1 <= h <= 12) else (h - 12 if h > 12 else 12)
            r['hora_formateada'] = f"{h12:02d}:{m:02d} {ampm}"
        elif hr:
            r['hora_formateada'] = str(hr)
        else:
            r['hora_formateada'] = '—'
            
        fec = r.get('fecha')
        if hasattr(fec, 'strftime'):
            r['fecha_formateada'] = fec.strftime('%d/%m/%Y')
        elif fec:
            r['fecha_formateada'] = str(fec)
        else:
            r['fecha_formateada'] = '—'
            
    return registros


def calcular_metricas_aprendiz(aprendiz_id):
    """Calcula las métricas de asistencia para el panel personal del aprendiz."""
    query = """
        SELECT estado, COUNT(*) as total
        FROM asistencias
        WHERE aprendiz_id = %s
        GROUP BY estado
    """
    resultados = ejecutar_consulta(query, (aprendiz_id,), fetchall=True) or []
    presentes = 0
    ausentes = 0
    corregidos = 0
    
    for r in resultados:
        if r['estado'] == 'presente':
            presentes += r['total']
        elif r['estado'] == 'ausente':
            ausentes += r['total']
        elif r['estado'] == 'corregido':
            corregidos += r['total']
            presentes += r['total']
            
    total = presentes + ausentes
    porcentaje = round((presentes / total * 100), 1) if total > 0 else 0
    
    return {
        'asistencias': presentes,
        'faltas': ausentes,
        'retardos': corregidos,
        'porcentaje': porcentaje
    }

