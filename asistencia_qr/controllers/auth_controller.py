from flask import Blueprint, request, render_template, redirect, url_for, session, abort
from functools import wraps
from models import usuario

auth_bp = Blueprint('auth', __name__)

def requiere_rol(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('auth.login', next=request.url))
            if session.get('rol') not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        documento = request.form.get('documento')
        password = request.form.get('password')
        
        user = usuario.autenticar(documento, password)
        if user:
            session['user_id'] = user['id']
            session['rol'] = user['rol']
            session['nombre'] = user['nombre']
            session['documento'] = user.get('documento', '')
            session['iniciales'] = ''.join([n[0] for n in user['nombre'].split()[:2]]).upper()
            
            next_url = request.args.get('next')
            if next_url:
                return redirect(next_url)
                
            if user['rol'] == 'instructor':
                return redirect(url_for('instructor.sesion'))
            elif user['rol'] == 'admin':
                return redirect(url_for('admin.panel'))
            elif user['rol'] == 'aprendiz':
                return redirect(url_for('aprendiz.escanear'))
        else:
            return render_template('login.html', error='Credenciales inválidas')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
