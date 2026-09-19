"""
Controlador de Administración — Gestión de usuarios, fichas, auditoría y configuración.
"""
from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify, flash
from controllers.auth_controller import requiere_rol
from models import usuario, auditoria, ficha
from models.dashboard import obtener_metricas_admin
from models.db import ejecutar_consulta
from controllers.seguridad import hash_password, obtener_ip_real

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/panel')
@requiere_rol('admin')
def panel():
    """Muestra el panel de administración con pestañas: dashboard, fichas, usuarios, auditoría, configuración."""
    # Filtros de Usuarios
    filtros_usuarios = {}
    if request.args.get('q'):
        filtros_usuarios['q'] = request.args.get('q').strip()
    if request.args.get('rol'):
        filtros_usuarios['rol'] = request.args.get('rol')
    if request.args.get('estado'):
        filtros_usuarios['estado'] = request.args.get('estado')

    # Filtros de Auditoría
    filtros_auditoria = {}
    if request.args.get('aud_q'):
        filtros_auditoria['q'] = request.args.get('aud_q').strip()
    if request.args.get('aud_accion'):
        filtros_auditoria['accion'] = request.args.get('aud_accion')
    if request.args.get('aud_resultado'):
        filtros_auditoria['resultado'] = request.args.get('aud_resultado')
    if request.args.get('aud_fecha_inicio'):
        filtros_auditoria['fecha_inicio'] = request.args.get('aud_fecha_inicio')
    if request.args.get('aud_fecha_fin'):
        filtros_auditoria['fecha_fin'] = request.args.get('aud_fecha_fin')
    if request.args.get('aud_usuario_id'):
        filtros_auditoria['usuario_id'] = request.args.get('aud_usuario_id')

    try:
        aud_pagina = int(request.args.get('aud_pagina', 1))
        if aud_pagina < 1:
            aud_pagina = 1
    except (ValueError, TypeError):
        aud_pagina = 1

    usuarios_lista = usuario.obtener_todos(filtros_usuarios)
    instructores_lista = usuario.obtener_todos({'rol': 'instructor', 'estado': 'activo'})
    logs = auditoria.obtener_log(filtros_auditoria, pagina=aud_pagina, por_pagina=20)
    fichas_lista = ficha.obtener_todas()
    metricas = obtener_metricas_admin()
    
    # Obtener configuración del sistema
    config = ejecutar_consulta("SELECT * FROM configuracion ORDER BY clave ASC", fetchall=True) or []
    
    # Pestaña activa inicial
    tab_activa = request.args.get('tab', 'dashboard')
    
    return render_template('admin/panel.html', 
                           usuarios=usuarios_lista, 
                           instructores=instructores_lista,
                           auditoria_log=logs, 
                           configuracion=config,
                           fichas=fichas_lista,
                           metricas=metricas,
                           tab_activa=tab_activa,
                           filtros_usuarios=filtros_usuarios,
                           filtros_auditoria=filtros_auditoria,
                           aud_pagina=aud_pagina)


@admin_bp.route('/admin/usuarios/crear', methods=['POST'])
@requiere_rol('admin')
def crear_usuario():
    """Crea un nuevo usuario en el sistema con validaciones."""
    nombre = (request.form.get('nombre') or '').strip()
    documento = (request.form.get('documento') or '').strip()
    password = (request.form.get('password') or 'sena2026').strip()
    rol = request.form.get('rol', 'instructor')
    centro = (request.form.get('centro') or 'Centro de la Industria, la Empresa y los Servicios - Neiva').strip()
    estado = request.form.get('estado', 'activo')
    
    if not nombre or not documento:
        flash('Nombre y documento son obligatorios para crear el usuario.', 'error')
        return redirect(url_for('admin.panel', tab='usuarios'))
        
    existente = usuario.obtener_por_documento(documento)
    if existente:
        flash(f'Ya existe un usuario registrado con el documento CC {documento}.', 'warning')
        return redirect(url_for('admin.panel', tab='usuarios'))
    
    pwd_hash = hash_password(password)
    usuario.crear(nombre, documento, pwd_hash, rol, centro, estado)
    
    ip = obtener_ip_real(request)
    auditoria.registrar(session['user_id'], ip, 'USUARIO_CREADO', 'exitoso', f'{nombre} ({documento}) — Rol: {rol}')
    
    flash(f'Usuario {nombre} (CC {documento}) creado exitosamente.', 'success')
    return redirect(url_for('admin.panel', tab='usuarios'))


@admin_bp.route('/admin/usuarios/editar/<int:id>', methods=['POST'])
@requiere_rol('admin')
def editar_usuario(id):
    """Edita los datos de un usuario existente, incluyendo reseteo de contraseña."""
    nombre = (request.form.get('nombre') or '').strip()
    documento = (request.form.get('documento') or '').strip()
    rol = request.form.get('rol')
    centro = (request.form.get('centro') or '').strip()
    estado = request.form.get('estado')
    password_nuevo = (request.form.get('password') or '').strip()
    
    datos = {}
    if nombre:
        datos['nombre'] = nombre
    if documento:
        datos['documento'] = documento
    if rol:
        datos['rol'] = rol
    if centro:
        datos['centro'] = centro
    if estado:
        datos['estado'] = estado
    if password_nuevo:
        datos['password'] = password_nuevo
    
    if datos:
        usuario.actualizar(id, datos)
        ip = obtener_ip_real(request)
        auditoria.registrar(session['user_id'], ip, 'USUARIO_EDITADO', 'exitoso', f'Usuario ID {id} actualizado.')
        flash('Usuario actualizado correctamente.', 'success')
    
    return redirect(url_for('admin.panel', tab='usuarios'))


@admin_bp.route('/admin/auditoria')
@requiere_rol('admin')
def api_auditoria():
    """API: Retorna el log de auditoría filtrado en formato JSON."""
    filtros = {}
    if request.args.get('usuario_id'):
        filtros['usuario_id'] = request.args.get('usuario_id')
    if request.args.get('accion'):
        filtros['accion'] = request.args.get('accion')
    if request.args.get('resultado'):
        filtros['resultado'] = request.args.get('resultado')
    if request.args.get('fecha_inicio'):
        filtros['fecha_inicio'] = request.args.get('fecha_inicio')
    if request.args.get('fecha_fin'):
        filtros['fecha_fin'] = request.args.get('fecha_fin')
    
    logs = auditoria.obtener_log(filtros)
    return jsonify(logs)


@admin_bp.route('/admin/config/guardar', methods=['POST'])
@requiere_rol('admin')
def guardar_config():
    """Guarda la configuración del sistema."""
    for clave in request.form:
        if clave not in ['csrf_token', 'tab']:
            valor = request.form.get(clave)
            ejecutar_consulta(
                "UPDATE configuracion SET valor = %s WHERE clave = %s",
                (valor, clave), commit=True
            )
    
    ip = obtener_ip_real(request)
    auditoria.registrar(session['user_id'], ip, 'CONFIG_ACTUALIZADA', 'exitoso', 'Parámetros del sistema modificados')
    
    flash('Configuración guardada correctamente.', 'success')
    return redirect(url_for('admin.panel', tab='config'))


# ============================================================
#  GESTIÓN DE FICHAS (ADMIN)
# ============================================================

@admin_bp.route('/admin/fichas/crear', methods=['POST'])
@requiere_rol('admin')
def crear_ficha():
    """Crea una nueva ficha de caracterización institucional."""
    numero = (request.form.get('numero') or '').strip()
    programa = (request.form.get('programa') or '').strip()
    sede = (request.form.get('sede') or 'Sede Principal - Neiva').strip()
    instructor_id = request.form.get('instructor_id')
    
    if not numero or not programa or not instructor_id:
        flash('Número de ficha, programa e instructor responsable son obligatorios.', 'error')
        return redirect(url_for('admin.panel', tab='fichas'))
        
    try:
        ficha.crear(numero, programa, sede, instructor_id)
        ip = obtener_ip_real(request)
        auditoria.registrar(session['user_id'], ip, 'FICHA_CREADA', 'exitoso', f'Ficha {numero} — {programa}')
        flash(f'Ficha {numero} creada exitosamente.', 'success')
    except Exception as e:
        flash(f'Error al crear ficha (puede que ya exista el número {numero}): {str(e)}', 'error')
        
    return redirect(url_for('admin.panel', tab='fichas'))


@admin_bp.route('/admin/fichas/estado', methods=['POST'])
@requiere_rol('admin')
def cambiar_estado_ficha():
    """Cambia el estado operativo de una ficha."""
    ficha_id = request.form.get('ficha_id')
    nuevo_estado = request.form.get('estado')
    
    if not ficha_id or not nuevo_estado:
        return redirect(url_for('admin.panel', tab='fichas'))
        
    datos = {'estado': nuevo_estado}
    if nuevo_estado in ['finalizada', 'archivada']:
        from datetime import date
        datos['fecha_cierre'] = date.today()
        
    ficha.actualizar(ficha_id, datos)
    
    ip = obtener_ip_real(request)
    auditoria.registrar(session['user_id'], ip, 'ESTADO_FICHA_CAMBIADO', 'exitoso', f'Ficha ID {ficha_id} -> {nuevo_estado}')
    flash(f'Estado de la ficha actualizado a "{nuevo_estado}".', 'success')
    return redirect(url_for('admin.panel', tab='fichas'))


