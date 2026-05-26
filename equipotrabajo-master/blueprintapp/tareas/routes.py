# Librerías a usar en el módulo
from flask import request, render_template, redirect, url_for, Blueprint, flash

# Referencia a la base de datos
from blueprintapp.app import db
# Modelos con los que interactúa el módulo
from blueprintapp.tareas.models import Tarea

bp_tarea = Blueprint('bp_tarea', __name__, template_folder='templates')

@bp_tarea.route("/")
def index():
    tareas = Tarea.query.all()
    return render_template('tareas/index.html', tareas=tareas)

@bp_tarea.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('tareas/create.html')
    elif request.method == 'POST':
        descripcion = request.form.get('descripcion')
        completado = True if 'completado' in request.form.keys() else False
        
        tarea = Tarea(descripcion=descripcion, completado=completado)
        db.session.add(tarea)
        db.session.commit()
        flash('✅ Tarea creada exitosamente', 'success')
        return redirect(url_for('bp_tarea.index'))

# NUEVA RUTA: EDITAR TAREA
@bp_tarea.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    tarea = Tarea.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('tareas/edit.html', tarea=tarea)
    elif request.method == 'POST':
        descripcion = request.form.get('descripcion')
        completado = True if 'completado' in request.form.keys() else False
        
        if not descripcion:
            flash('⚠️ La descripción es obligatoria', 'warning')
            return redirect(url_for('bp_tarea.edit', id=id))
        
        tarea.descripcion = descripcion
        tarea.completado = completado
        db.session.commit()
        flash('✅ Tarea actualizada', 'success')
        return redirect(url_for('bp_tarea.index'))

#  NUEVA RUTA: ELIMINAR TAREA
@bp_tarea.route("/delete/<int:id>")
def delete(id):
    tarea = Tarea.query.get_or_404(id)
    db.session.delete(tarea)
    db.session.commit()
    flash('🗑️ Tarea eliminada', 'info')
    return redirect(url_for('bp_tarea.index'))