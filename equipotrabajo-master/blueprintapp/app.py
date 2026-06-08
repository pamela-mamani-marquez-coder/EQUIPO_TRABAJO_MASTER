from flask import Flask, render_template, redirect, url_for, flash 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 
from flask_bcrypt import Bcrypt       
from flask_login import current_user


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager() 
bcrypt = Bcrypt()             

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__, template_folder='templates')
    

    app.config['SECRET_KEY'] = 'equipo_trabajo_clave_secreta_2026' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_equipo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app) 
    bcrypt.init_app(app)        
    
    # Configuración de Login Manager
    login_manager.login_view = 'bp_auth.login' # Ruta a la que redirige si no hay sesión
    login_manager.login_message = 'Por favor, inicia sesión para acceder.'
    login_manager.login_message_category = 'info'

 
   
    from blueprintapp.auth.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar Blueprints Existentes
    from blueprintapp.miembros.routes import bp_miembro
    from blueprintapp.core.routes import bp_core
    from blueprintapp.tareas.routes import bp_tarea
    from blueprintapp.auth.routes import bp_auth
    
    # NUEVO: Importar y Registrar el Blueprint de Autenticación
    from blueprintapp.auth.routes import bp_auth
    
    app.register_blueprint(bp_miembro, url_prefix='/miembros')
    app.register_blueprint(bp_core, url_prefix='/')  
    app.register_blueprint(bp_tarea, url_prefix='/tareas')
    app.register_blueprint(bp_auth, url_prefix='/auth') 
    

    @app.route('/')
    def home():
        return render_template('core/index.html') 
    
 
    with app.app_context():
        db.create_all()
        print("✅ Base de datos 'bd_equipo.db' verificada/creada exitosamente")
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)