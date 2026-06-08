from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required 
from blueprintapp.app import db
from blueprintapp.miembros.models import Miembro


bp_miembro = Blueprint('bp_miembro', __name__, template_folder='templates/miembro')

@bp_miembro.route("/")
@login_required 
def index():
    """Muestra la lista de todos los miembros."""
    miembros = Miembro.query.all()
    return render_template('index.html', miembros=miembros)

@bp_miembro.route("/create", methods=['GET', 'POST'])
@login_required 
def create():
    """Crea un nuevo miembro."""
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        
        # Validación básica
        if not nombre or not email:
            flash('⚠️ Nombre y email son obligatorios', 'warning')
            return redirect(url_for('bp_miembro.create'))
        
        # Crear y guardar en BD
        nuevo_miembro = Miembro(nombre=nombre, email=email)
        db.session.add(nuevo_miembro)
        db.session.commit()
        
        flash('✅ Miembro creado exitosamente', 'success')
        return redirect(url_for('bp_miembro.index'))

@bp_miembro.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required 
def edit(id):
    """Edita un miembro existente."""
    miembro = Miembro.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('edit.html', miembro=miembro)
    elif request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        
        if not nombre or not email:
            flash('⚠️ Nombre y email son obligatorios', 'warning')
            return redirect(url_for('bp_miembro.edit', id=id))
        
        # Actualizar datos
        miembro.nombre = nombre
        miembro.email = email
        db.session.commit()
        
        flash('✅ Miembro actualizado correctamente', 'success')
        return redirect(url_for('bp_miembro.index'))

@bp_miembro.route("/delete/<int:id>")
@login_required 
def delete(id):
    """Elimina un miembro."""
    miembro = Miembro.query.get_or_404(id)
    db.session.delete(miembro)
    db.session.commit()
    
    flash('🗑️ Miembro eliminado correctamente', 'info')
    return redirect(url_for('bp_miembro.index'))