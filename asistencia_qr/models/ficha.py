from models.db import ejecutar_consulta
from datetime import date

def obtener_todas(estado=None):
    if estado:
        query = "SELECT * FROM fichas WHERE estado = %s ORDER BY id DESC"
        return ejecutar_consulta(query, (estado,), fetchall=True)
    return ejecutar_consulta("SELECT * FROM fichas ORDER BY id DESC", fetchall=True)

def obtener_por_id(id):
    query = "SELECT * FROM fichas WHERE id = %s"
    return ejecutar_consulta(query, (id,), fetchone=True)

def obtener_por_instructor(instructor_id, estado=None):
    if estado:
        query = "SELECT * FROM fichas WHERE instructor_id = %s AND estado = %s"
        return ejecutar_consulta(query, (instructor_id, estado), fetchall=True)
    query = "SELECT * FROM fichas WHERE instructor_id = %s"
    return ejecutar_consulta(query, (instructor_id,), fetchall=True)

def crear(numero, programa, sede, instructor_id):
    query = """
        INSERT INTO fichas (numero, programa, sede, instructor_id, estado, fecha_apertura)
        VALUES (%s, %s, %s, %s, 'activa', %s)
    """
    return ejecutar_consulta(query, (numero, programa, sede, instructor_id, date.today()), commit=True)

def actualizar(id, datos):
    if not datos:
        return False
    campos = []
    params = []
    for k, v in datos.items():
        campos.append(f"{k} = %s")
        params.append(v)
    params.append(id)
    query = f"UPDATE fichas SET {', '.join(campos)} WHERE id = %s"
    ejecutar_consulta(query, tuple(params), commit=True)
    return True

def obtener_aprendices(ficha_id):
    query = """
        SELECT u.* FROM usuarios u
        JOIN ficha_aprendiz fa ON u.id = fa.aprendiz_id
        WHERE fa.ficha_id = %s
    """
    return ejecutar_consulta(query, (ficha_id,), fetchall=True)

def aprendiz_pertenece(aprendiz_id, ficha_id):
    query = "SELECT 1 FROM ficha_aprendiz WHERE aprendiz_id = %s AND ficha_id = %s"
    resultado = ejecutar_consulta(query, (aprendiz_id, ficha_id), fetchone=True)
    return resultado is not None

def vincular_aprendiz(ficha_id, aprendiz_id):
    """Vincula un aprendiz a una ficha para que quede registrado en el sistema."""
    query = "INSERT IGNORE INTO ficha_aprendiz (ficha_id, aprendiz_id) VALUES (%s, %s)"
    return ejecutar_consulta(query, (ficha_id, aprendiz_id), commit=True)


