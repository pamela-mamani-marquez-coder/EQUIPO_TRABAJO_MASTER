from blueprintapp.app import db

class Tarea(db.Model):
    __tablename__ = "tareas"
    
    id = db.Column(db.Integer, primary_key=True)
    descripcion =  db.Column(db.String, nullable=False)
    completado = db.Column(db.Boolean,nullable=False)
    
    def __repr__(self):
        return f"<TAREA: {self.descripcion} - {self.completado}"
