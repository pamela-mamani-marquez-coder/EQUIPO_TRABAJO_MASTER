from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from blueprintapp.app import db, bcrypt
from blueprintapp.auth.models import Usuario
from blueprintapp.auth import bp_auth

# Ruta de LOGIN
@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Buscamos el usuario por nombre
        user = Usuario.query.filter_by(username=username).first()
        
        # Verificamos si existe y si la contraseña coincide 
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user) # Iniciamos la sesión
            flash('✅ Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('❌ Usuario o contraseña incorrectos', 'danger')
            
    return render_template('auth/login.html')

# Ruta de REGISTRO
@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verificar si el usuario ya existe
        if Usuario.query.filter_by(username=username).first():
            flash('⚠️ El nombre de usuario ya existe', 'warning')
            return redirect(url_for('bp_auth.register'))
            
        # Encriptar la contraseña antes de guardarla
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = Usuario(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('✅ Usuario registrado. Por favor inicia sesión.', 'success')
        return redirect(url_for('bp_auth.login'))
        
    return render_template('auth/register.html')

# Ruta de LOGOUT
@bp_auth.route('/logout')
@login_required 
def logout():
    logout_user()
    flash('👋 Sesión cerrada correctamente', 'info')
    return redirect(url_for('home'))