from models.db import ejecutar_consulta

def registrar(usuario_id, ip_origen, accion, resultado, detalle):
    query = """
        INSERT INTO auditoria (usuario_id, ip_origen, accion, resultado, detalle)
        VALUES (%s, %s, %s, %s, %s)
    """
    return ejecutar_consulta(query, (usuario_id, ip_origen, accion, resultado, detalle), commit=True)

def obtener_log(filtros=None, pagina=1, por_pagina=20):
    if filtros is None:
        filtros = {}
        
    query_base = """
        FROM auditoria a
        LEFT JOIN usuarios u ON a.usuario_id = u.id
        WHERE 1=1
    """
    params = []
    
    if filtros.get('usuario_id'):
        query_base += " AND a.usuario_id = %s"
        params.append(filtros['usuario_id'])
    if filtros.get('accion'):
        query_base += " AND a.accion = %s"
        params.append(filtros['accion'])
    if filtros.get('resultado'):
        query_base += " AND a.resultado = %s"
        params.append(filtros['resultado'])
    if filtros.get('fecha_inicio'):
        query_base += " AND a.created_at >= %s"
        params.append(f"{filtros['fecha_inicio']} 00:00:00")
    if filtros.get('fecha_fin'):
        query_base += " AND a.created_at <= %s"
        params.append(f"{filtros['fecha_fin']} 23:59:59")
    if filtros.get('q'):
        query_base += " AND (a.detalle LIKE %s OR u.nombre LIKE %s OR a.accion LIKE %s)"
        param_q = f"%{filtros['q'].strip()}%"
        params.extend([param_q, param_q, param_q])
        
    query_count = f"SELECT COUNT(*) as total {query_base}"
    total_res = ejecutar_consulta(query_count, tuple(params), fetchone=True)
    total = total_res['total'] if total_res else 0
    
    query_data = f"""
        SELECT a.*, u.nombre as usuario_nombre, u.documento as usuario_documento
        {query_base}
        ORDER BY a.created_at DESC
        LIMIT %s OFFSET %s
    """
    offset = max(0, (pagina - 1) * por_pagina)
    params_data = list(params) + [por_pagina, offset]
    
    registros = ejecutar_consulta(query_data, tuple(params_data), fetchall=True) or []
    
    return {'registros': registros, 'total': total}
