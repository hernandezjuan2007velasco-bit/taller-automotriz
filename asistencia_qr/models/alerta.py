from models.db import ejecutar_consulta

def obtener_por_instructor(instructor_id):
    query = """
        SELECT a.*, u.nombre as aprendiz_nombre, u.documento as aprendiz_documento, f.numero as ficha_numero
        FROM alertas a
        JOIN usuarios u ON a.aprendiz_id = u.id
        JOIN fichas f ON a.ficha_id = f.id
        WHERE f.instructor_id = %s
        ORDER BY a.created_at DESC
    """
    return ejecutar_consulta(query, (instructor_id,), fetchall=True)

def contar_activas(instructor_id):
    query = """
        SELECT 
            SUM(CASE WHEN a.estado = 'activa' THEN 1 ELSE 0 END) as total,
            SUM(CASE WHEN a.estado = 'activa' AND a.tipo = 'riesgo_alto' THEN 1 ELSE 0 END) as riesgo_alto,
            SUM(CASE WHEN a.estado = 'atendida' AND MONTH(a.created_at) = MONTH(CURRENT_DATE()) AND YEAR(a.created_at) = YEAR(CURRENT_DATE()) THEN 1 ELSE 0 END) as atendidas_mes
        FROM alertas a
        JOIN fichas f ON a.ficha_id = f.id
        WHERE f.instructor_id = %s
    """
    resultado = ejecutar_consulta(query, (instructor_id,), fetchone=True)
    return {
        'total': int(resultado['total'] or 0),
        'riesgo_alto': int(resultado['riesgo_alto'] or 0),
        'atendidas_mes': int(resultado['atendidas_mes'] or 0)
    }

def atender(alerta_id, nota):
    query = "UPDATE alertas SET estado = 'atendida', nota_seguimiento = %s WHERE id = %s"
    ejecutar_consulta(query, (nota, alerta_id), commit=True)
    return True
