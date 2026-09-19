"""
Controlador del Aprendiz — Flujo de registro de asistencia con ingreso de cédula, nombres completos y validación anti-fraude.
"""
from flask import Blueprint, request, render_template, session, jsonify
from datetime import datetime, date
from controllers.auth_controller import requiere_rol
from models import ficha, sesion as modelo_sesion, asistencia, auditoria, usuario
from controllers.seguridad import verificar_codigo_qr, misma_subred, obtener_ip_real, hash_password
from config import Config

aprendiz_bp = Blueprint('aprendiz', __name__)


@aprendiz_bp.route('/aprendiz/escanear')
def escanear():
    """
    Muestra la vista para que el aprendiz ingrese o confirme su asistencia.
    Acceso público: no requiere inicio de sesión previo para no bloquear aprendices en el aula.
    """
    codigo = request.args.get('codigo', '')
    return render_template('aprendiz/escanear.html', codigo_url=codigo)


@aprendiz_bp.route('/aprendiz/buscar-documento/<doc>')
def buscar_documento(doc):
    """
    API de conveniencia: si el aprendiz ya existe en el sistema,
    autocompleta sus nombres completos al digitar la cédula.
    """
    documento_limpio = doc.strip()
    if not documento_limpio:
        return jsonify({'encontrado': False})
        
    user = usuario.obtener_por_documento(documento_limpio)
    if user:
        return jsonify({
            'encontrado': True,
            'nombre': user.get('nombre', ''),
            'rol': user.get('rol', '')
        })
    return jsonify({'encontrado': False})


@aprendiz_bp.route('/aprendiz/confirmar', methods=['POST'])
def confirmar():
    """
    Endpoint principal de registro de asistencia.
    Recibe cédula, nombres completos y código QR.
    
    Acciones garantizadas:
    1. Validar código QR (HMAC dinámico + ventana de tiempo vigente).
    2. Validar sesión activa en la ficha.
    3. Validar red local institucional si está habilitada en configuración.
    4. Auto-registrar o actualizar al aprendiz en la tabla 'usuarios' (sin pérdida de datos).
    5. Vincular al aprendiz con la ficha correspondiente en 'ficha_aprendiz'.
    6. Validar que no se duplique la asistencia en la misma sesión.
    7. Registrar asistencia en la tabla 'asistencias' (hora, fecha, IP).
    8. Registrar trazabilidad completa en 'auditoria'.
    9. Autenticar la sesión en el navegador del aprendiz.
    """
    datos = request.get_json(silent=True) if request.is_json else request.form
    if not datos:
        return jsonify({'exito': False, 'mensaje': 'Datos de registro no recibidos', 'datos': {}}), 400

    codigo = (datos.get('codigo') or '').strip()
    documento = (datos.get('documento') or '').strip()
    nombre = (datos.get('nombre') or '').strip()

    # Validaciones iniciales de campos
    if not codigo:
        return jsonify({'exito': False, 'mensaje': 'El código de sesión es obligatorio.', 'datos': {}}), 400
    if not documento:
        return jsonify({'exito': False, 'mensaje': 'Por favor ingresa tu número de documento o cédula.', 'datos': {}}), 400
    if not nombre or len(nombre) < 3:
        return jsonify({'exito': False, 'mensaje': 'Por favor ingresa tus nombres y apellidos completos.', 'datos': {}}), 400

    client_ip = obtener_ip_real(request)

    # PASO 1: Verificar código QR con HMAC y tolerancia de rotación
    sesion_id = verificar_codigo_qr(codigo, Config.QR_HMAC_SECRET, Config.QR_TOLERANCIA_PERIODOS)
    if not sesion_id:
        return jsonify({
            'exito': False,
            'mensaje': 'El código QR es inválido o ya expiró (rota cada 30s). Escanea el nuevo código en pantalla.',
            'datos': {}
        })

    # PASO 2: Verificar que la sesión de formación esté activa
    sesion_obj = modelo_sesion.obtener_por_id(sesion_id)
    if not sesion_obj or sesion_obj.get('estado') != 'activa':
        return jsonify({
            'exito': False,
            'mensaje': 'La ventana de registro ya fue cerrada por el instructor.',
            'datos': {}
        })

    # PASO 3: Verificar política de red local (si está activada en producción)
    if Config.VALIDAR_RED:
        ip_instructor = sesion_obj.get('ip_instructor', '')
        if not misma_subred(ip_instructor, client_ip, Config.MASCARA_SUBRED):
            auditoria.registrar(
                None, client_ip, 'INTENTO_REGISTRO', 'fallido',
                f'Red diferente. Instructor: {ip_instructor}, Aprendiz: {client_ip}'
            )
            return jsonify({
                'exito': False,
                'mensaje': 'Debes estar conectado a la misma red Wi-Fi del aula para registrar asistencia.',
                'datos': {}
            })

    # PASO 4: Buscar o auto-registrar al aprendiz en 'usuarios'
    user = usuario.obtener_por_documento(documento)
    if not user:
        # Nuevo aprendiz: crearlo con rol aprendiz y contraseña estándar sena2026
        pwd_hash = hash_password('sena2026')
        nuevo_id = usuario.crear(
            nombre=nombre,
            documento=documento,
            password_hash=pwd_hash,
            rol='aprendiz',
            centro='Centro de la Industria, la Empresa y los Servicios - Neiva',
            estado='activo'
        )
        user = usuario.obtener_por_id(nuevo_id)
        auditoria.registrar(user['id'], client_ip, 'USUARIO_CREADO', 'exitoso', f'Auto-registro aprendiz: {nombre} (CC {documento})')
    else:
        # Si ya existe y escribió un nombre más completo o corregido, actualizarlo
        if nombre and len(nombre) >= len(user.get('nombre', '')) and user.get('nombre') != nombre:
            usuario.actualizar(user['id'], {'nombre': nombre})
            user['nombre'] = nombre

    aprendiz_id = user['id']
    ficha_id = sesion_obj['ficha_id']

    # PASO 5: Vincular permanentemente al aprendiz con la ficha si aún no lo estaba
    if not ficha.aprendiz_pertenece(aprendiz_id, ficha_id):
        ficha.vincular_aprendiz(ficha_id, aprendiz_id)
        auditoria.registrar(aprendiz_id, client_ip, 'VINCULACION_FICHA', 'exitoso', f'Aprendiz {documento} vinculado a Ficha {ficha_id}')

    # PASO 6: Validar que no haya duplicado en la misma sesión
    if asistencia.ya_registro(sesion_id, aprendiz_id):
        auditoria.registrar(aprendiz_id, client_ip, 'INTENTO_REGISTRO', 'fallido', 'Registro duplicado')
        return jsonify({
            'exito': False,
            'mensaje': f'Ya registraste tu asistencia para esta sesión hoy, {user["nombre"]}.',
            'datos': {}
        })

    # PASO 7: Guardar el registro de asistencia en la base de datos
    asistencia.registrar(sesion_id, aprendiz_id, client_ip)
    auditoria.registrar(aprendiz_id, client_ip, 'ASISTENCIA_REGISTRADA', 'exitoso', f'Sesión {sesion_id}, Ficha {ficha_id}')

    # PASO 8: Iniciar sesión en el navegador del aprendiz para su conveniencia
    session['user_id'] = user['id']
    session['rol'] = 'aprendiz'
    session['nombre'] = user['nombre']
    session['documento'] = user['documento']
    session['iniciales'] = ''.join([n[0] for n in user['nombre'].split()[:2]]).upper()

    # PASO 9: Obtener datos de la ficha para la pantalla de éxito
    ficha_obj = ficha.obtener_por_id(ficha_id)
    ficha_texto = f"Ficha {ficha_obj['numero']} — {ficha_obj['programa']}" if ficha_obj else f"Ficha {ficha_id}"

    return jsonify({
        'exito': True,
        'mensaje': '¡Asistencia registrada correctamente!',
        'datos': {
            'nombre': user['nombre'],
            'documento': user['documento'],
            'ficha': ficha_texto,
            'hora': datetime.now().strftime('%I:%M:%S %p'),
            'fecha': date.today().strftime('%d/%m/%Y')
        }
    })

@aprendiz_bp.route('/aprendiz/historial')
@requiere_rol('aprendiz')
def historial():
    """Muestra el panel y el historial de asistencia del aprendiz."""
    aprendiz_id = session['user_id']
    registros = asistencia.obtener_historial_aprendiz(aprendiz_id)
    metricas = asistencia.calcular_metricas_aprendiz(aprendiz_id)
    return render_template('aprendiz/historial.html', registros=registros, metricas=metricas)
