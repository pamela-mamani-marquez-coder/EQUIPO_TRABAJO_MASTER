# Librerías a usar en el módulo
from flask import request, render_template, redirect, url_for, Blueprint, flash

# Referencia a la base de datos
from blueprintapp.app import db
# Modelos con los que interactúa el módulo
from blueprintapp.miembros.models import Miembro

bp_miembro = Blueprint('bp_miembro', __name__, template_folder='templates')

@bp_miembro.route("/")
def index():
    miembros = Miembro.query.all()
    return render_template('miembro/index.html', miembros=miembros)

@bp_miembro.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('miembro/create.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        
        if not nombre or not email:
            flash('⚠️ Nombre y email son obligatorios', 'warning')
            return redirect(url_for('bp_miembro.create'))
        
        miembro = Miembro(nombre=nombre, email=email)
        db.session.add(miembro)
        db.session.commit()
        flash('✅ Miembro creado exitosamente', 'success')
        return redirect(url_for('bp_miembro.index'))

#  NUEVA RUTA: EDITAR
@bp_miembro.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    miembro = Miembro.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('miembro/edit.html', miembro=miembro)
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        
        if not nombre or not email:
            flash('⚠️ Nombre y email son obligatorios', 'warning')
            return redirect(url_for('bp_miembro.edit', id=id))
        
        miembro.nombre = nombre
        miembro.email = email
        db.session.commit()
        flash('✅ Miembro actualizado', 'success')
        return redirect(url_for('bp_miembro.index'))

# NUEVA RUTA: ELIMINAR
@bp_miembro.route("/delete/<int:id>")
def delete(id):
    miembro = Miembro.query.get_or_404(id)
    db.session.delete(miembro)
    db.session.commit()
    flash('🗑️ Miembro eliminado', 'info')
    return redirect(url_for('bp_miembro.index'))