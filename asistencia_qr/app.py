from flask import Flask, redirect, url_for, session, render_template_string
from config import Config
from models.db import DatabaseConnectionError
import logging

def crear_app():
    app = Flask(__name__, 
                template_folder='views',
                static_folder='static')
    app.config.from_object(Config)
    
    # Register blueprints
    from controllers.auth_controller import auth_bp
    from controllers.instructor_controller import instructor_bp
    from controllers.aprendiz_controller import aprendiz_bp
    from controllers.admin_controller import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(instructor_bp)
    app.register_blueprint(aprendiz_bp)
    app.register_blueprint(admin_bp)
    
    @app.route('/')
    def index():
        if 'user_id' in session:
            rol = session.get('rol')
            if rol == 'instructor':
                return redirect(url_for('instructor.sesion'))
            elif rol == 'admin':
                return redirect(url_for('admin.panel'))
            elif rol == 'aprendiz':
                return redirect(url_for('aprendiz.escanear'))
        return redirect(url_for('auth.login'))
    
    # Context processor for templates
    @app.context_processor
    def inject_user():
        return {
            'usuario_actual': {
                'id': session.get('user_id'),
                'nombre': session.get('nombre'),
                'documento': session.get('documento'),
                'rol': session.get('rol'),
                'iniciales': session.get('iniciales', '')
            } if 'user_id' in session else None
        }
    
    @app.errorhandler(DatabaseConnectionError)
    def handle_db_error(e):
        if app.config.get('DEBUG'):
            return f"<h1>Error de Base de Datos</h1><p>{str(e)}</p>", 500
        else:
            app.logger.error(f"Database error: {str(e)}")
            return "<h2>Lo sentimos</h2><p>No fue posible conectar con la base de datos.</p>", 500
            
    return app

# Exponer la aplicación a nivel de módulo para Gunicorn
app = crear_app()

if __name__ == '__main__':
    app.run(debug=app.config.get('DEBUG', False), host='0.0.0.0', port=5000)
