from app import app
from flask import render_template

with app.test_request_context('/'):
    # 1. Login
    try:
        render_template('login.html', error=None)
        print('✔ login.html renders fine')
    except Exception as e:
        print('❌ Error in login.html:', e)

    # 2. Instructor Sesion (Inactiva)
    try:
        render_template('instructor/sesion.html', fichas=[{'id':1,'numero':'2694582','programa':'ADSO'}], sesion_activa=None, metricas={'total_fichas':1, 'total_sesiones':5, 'asistencia_promedio':95.0, 'sesiones_activas':0}, url_compartir='http://localhost:5000')
        print('✔ instructor/sesion.html (inactiva) renders fine')
    except Exception as e:
        print('❌ Error in instructor/sesion.html (inactiva):', e)

    # 3. Instructor Sesion (Activa)
    try:
        sesion_mock = {'id': 1, 'ficha_id': 1, 'ficha_numero': '2694582', 'ficha_programa': 'ADSO', 'hora_inicio': '08:00 AM'}
        render_template('instructor/sesion.html', fichas=[], sesion_activa=sesion_mock, metricas={}, url_compartir='http://localhost:5000')
        print('✔ instructor/sesion.html (activa) renders fine')
    except Exception as e:
        print('❌ Error in instructor/sesion.html (activa):', e)
        
    # 4. Instructor Historial
    try:
        reg_mock = [{'id': 1, 'nombre': 'Juan Perez', 'documento': '1075000001', 'iniciales': 'JP', 'ficha_numero': '2694582', 'ficha_programa': 'ADSO', 'programa': 'ADSO', 'fecha_formateada': '19/09/2026', 'hora_formateada': '08:05 am', 'estado': 'presente', 'motivo_correccion': None}]
        render_template('instructor/historial.html', registros=reg_mock, total=1, total_paginas=1, pagina=1, por_pagina=15, metricas={'sesiones_total':1,'asistentes':1,'inasistentes':0,'porcentaje':100.0}, fichas=[], sesiones=[], filtros={'ficha_id':'','q':'','fecha_inicio':'','fecha_fin':'','estado':''})
        print('✔ instructor/historial.html renders fine')
    except Exception as e:
        print('❌ Error in instructor/historial.html:', e)

    # 5. Instructor Alertas
    try:
        alerta_mock = [{'id': 1, 'aprendiz_nombre': 'Pedro Gomez', 'aprendiz_documento': '1075000003', 'ficha_numero': '2694582', 'tipo': 'riesgo_alto', 'descripcion': '3 faltas consecutivas', 'porcentaje_riesgo': 80}]
        render_template('instructor/alertas.html', alertas=alerta_mock, metricas={'total':1, 'riesgo_alto':1, 'atendidas_mes':0})
        print('✔ instructor/alertas.html renders fine')
    except Exception as e:
        print('❌ Error in instructor/alertas.html:', e)

    # 6. Aprendiz Escanear
    try:
        render_template('aprendiz/escanear.html', codigo_url='1-59658624-5828AC16')
        print('✔ aprendiz/escanear.html renders fine')
    except Exception as e:
        print('❌ Error in aprendiz/escanear.html:', e)

    # 7. Aprendiz Historial
    try:
        render_template('aprendiz/historial.html', registros=[], metricas={'asistencias':10, 'faltas':1, 'retardos':0, 'porcentaje':90.9})
        print('✔ aprendiz/historial.html renders fine')
    except Exception as e:
        print('❌ Error in aprendiz/historial.html:', e)
        
    # 8. Admin Panel
    try:
        usr_mock = [{'id': 1, 'nombre': 'Administrador General', 'documento': '1075000001', 'rol': 'admin', 'centro': 'SENA Neiva', 'estado': 'activo'}]
        fch_mock = [{'id': 1, 'numero': '2694582', 'programa': 'ADSO', 'sede': 'Neiva', 'fecha_apertura': '2026-01-15', 'estado': 'activa'}]
        render_template('admin/panel.html', 
                        usuarios=usr_mock, 
                        instructores=usr_mock, 
                        auditoria_log={'registros':[{'id':1,'created_at':'2026-09-19 08:00:00','usuario_nombre':'Admin','ip_origen':'127.0.0.1','accion':'SESION_CREADA','resultado':'exitoso','detalle':'OK'}],'total':1}, 
                        configuracion=[{'clave':'qr_rotacion_segundos','valor':'30','descripcion':'Rotación QR'}], 
                        fichas=fch_mock, 
                        metricas={'total_aprendices':50,'total_instructores':5,'fichas_activas':3,'sesiones_activas':1,'asistencias_hoy':25,'alertas_activas':2},
                        tab_activa='dashboard',
                        filtros_usuarios={},
                        filtros_auditoria={},
                        aud_pagina=1)
        print('✔ admin/panel.html renders fine')
    except Exception as e:
        print('❌ Error in admin/panel.html:', e)

