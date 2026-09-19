"""
Modelo de Usuario — Gestión de instructores, administradores y aprendices.
"""
from models.db import ejecutar_consulta
from werkzeug.security import generate_password_hash, check_password_hash


def obtener_por_id(id):
    """Obtiene un usuario por su ID."""
    query = "SELECT * FROM usuarios WHERE id = %s"
    return ejecutar_consulta(query, (id,), fetchone=True)


def obtener_por_documento(documento):
    """Obtiene un usuario por su número de documento."""
    query = "SELECT * FROM usuarios WHERE documento = %s"
    return ejecutar_consulta(query, (documento,), fetchone=True)


def obtener_todos(filtros=None):
    """Obtiene todos los usuarios, opcionalmente filtrados por texto (q), rol, estado o centro."""
    if filtros is None:
        filtros = {}
    
    query = "SELECT * FROM usuarios WHERE 1=1"
    params = []
    
    if filtros.get('q'):
        query += " AND (nombre LIKE %s OR documento LIKE %s)"
        param_q = f"%{filtros['q'].strip()}%"
        params.extend([param_q, param_q])
    if filtros.get('rol'):
        query += " AND rol = %s"
        params.append(filtros['rol'])
    if filtros.get('estado'):
        query += " AND estado = %s"
        params.append(filtros['estado'])
    if filtros.get('centro'):
        query += " AND centro = %s"
        params.append(filtros['centro'])
    
    query += " ORDER BY nombre ASC"
    return ejecutar_consulta(query, tuple(params), fetchall=True)


def crear(nombre, documento, password_hash, rol, centro, estado='activo'):
    """Crea un nuevo usuario. Recibe el password ya hasheado."""
    query = """
        INSERT INTO usuarios (nombre, documento, password_hash, rol, centro, estado) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    return ejecutar_consulta(query, (nombre, documento, password_hash, rol, centro, estado), commit=True)


def actualizar(id, datos):
    """Actualiza los datos de un usuario. Recibe un diccionario con los campos a actualizar."""
    if not datos:
        return False
        
    campos = []
    params = []
    for key, value in datos.items():
        if key == 'password':
            campos.append("password_hash = %s")
            params.append(generate_password_hash(value))
        else:
            campos.append(f"{key} = %s")
            params.append(value)
            
    params.append(id)
    query = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = %s"
    ejecutar_consulta(query, tuple(params), commit=True)
    return True


def autenticar(documento, password):
    """Autentica un usuario. Retorna el usuario si las credenciales son válidas, None si no."""
    user = obtener_por_documento(documento)
    if user and user.get('estado') == 'activo' and check_password_hash(user['password_hash'], password):
        return user
    return None
