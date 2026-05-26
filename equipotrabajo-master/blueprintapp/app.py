from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__, template_folder='templates')
    
    # 🔑 Configuración CRÍTICA
    app.config['SECRET_KEY'] = 'equipo_trabajo_clave_secreta_2026' 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_equipo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 📦 Registrar Blueprints
    from blueprintapp.miembros.routes import bp_miembro
    from blueprintapp.core.routes import bp_core
    from blueprintapp.tareas.routes import bp_tarea
    
    app.register_blueprint(bp_miembro, url_prefix='/miembros')
    app.register_blueprint(bp_core, url_prefix='/')  # Core en la raíz
    app.register_blueprint(bp_tarea, url_prefix='/tareas')
    
  
    @app.route('/')
    def home():
        return redirect(url_for('bp_miembro.index'))
    
    # 🗄️ Crear tablas 
 
    with app.app_context():
        db.create_all()
        print("✅ Base de datos 'bd_equipo.db' creada exitosamente")
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)