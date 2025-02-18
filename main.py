from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from datetime import datetime
from forms import RegistroDueñoForm
from models_veterinaria import db, Dueño, Mascota, Veterinario, Tratamiento
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')

# Inicializamos la base de datos
db.init_app(app)

# Inicializamos Migrate
migrate = Migrate(app, db)

# Configurar la clave secreta para Flash
app.secret_key = 'mysecretkey'

# Inicialización de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Dueño.query.get(int(user_id))

# Función para crear el usuario admin
def create_admin():
    # Verificar si ya existe el usuario admin
    admin = Dueño.query.filter_by(correo='admin').first()
    
    if not admin:
        admin_password = generate_password_hash('admin')  
        admin = Dueño(
            cedula='123456789',  # Agregar un valor válido para la cédula
            nombre='Administrador',
            correo='admin',
            telefono='0000000000',
            password_hash=admin_password,  
            is_admin=True  # Asegúrate de usar 'is_admin', no 'es_admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuario admin creado")

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.is_admin:
        return render_template('admin_dashboard.html')  # Panel de administración
    else:
        flash('No tienes permiso para acceder a esta sección', 'error')
        return redirect(url_for('index'))


# Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Página de servicios
@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/citas')
@login_required
def citas():
    return render_template('citas.html')

@app.route('/consulta_virtual')
@login_required
def consulta_virtual():
    return render_template('consulta_virtual.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/gestion_inventario')
def gestion_inventario():
    return render_template('gestion_inventario.html')

@app.route('/recordatorios')
@login_required
def recordatorios():
    return render_template('recordatorios.html')

@app.route('/portal_educativo')
def portal_educativo():
    return render_template('portal_educativo.html')


# Ruta para registrar una mascota
@app.route('/registro', methods=['GET', 'POST'])
@login_required  # Aseguramos que el dueño esté autenticado
def registro():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            especie = request.form['especie']
            edad = request.form['edad']
            veterinario_id = request.form['veterinario']

            if not nombre or not especie or not edad or not veterinario_id:
                flash("Todos los campos son obligatorios.", "error")
                return render_template('registro.html')

            veterinario = Veterinario.query.get(veterinario_id)
            if not veterinario:
                flash("Veterinario no encontrado.", "error")
                return render_template('registro.html')

            nueva_mascota = Mascota(
                nombre=nombre, 
                especie=especie, 
                edad=edad, 
                veterinario_id=veterinario_id, 
                dueño_id=current_user.id  # Asocia la mascota al dueño autenticado
            )
            db.session.add(nueva_mascota)
            db.session.commit()

            flash("Mascota registrada correctamente", "success")
            return redirect(url_for('registro'))
        except Exception as e:
            flash(f"Error: {e}", "error")
            return render_template('registro.html')

    veterinarios = Veterinario.query.all()
    return render_template('registro.html', veterinarios=veterinarios)

# Ruta para el formulario de contacto
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            email = request.form['email']
            mensaje = request.form['mensaje']

            if not nombre or not email or not mensaje:
                flash("Todos los campos son obligatorios.", "error")
                return render_template('contacto.html')

            flash("Mensaje enviado correctamente", "success")
            return render_template('contacto.html')
        except Exception as e:
            flash(f"Error: {e}", "error")
            return render_template('contacto.html')

    return render_template('contacto.html')

# Ruta para ver las mascotas del dueño
@app.route('/mis_mascotas')
@login_required
def mis_mascotas():
    if current_user.is_authenticated:
        mascotas = Mascota.query.filter_by(dueño_id=current_user.id).all()
        return render_template('mis_mascotas.html', mascotas=mascotas)
    else:
        flash("Debes iniciar sesión para ver tus mascotas", "error")
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login_unificado():
    if request.method == 'POST':
        form_type = request.form.get('form_type')  # Saber si es login o registro

        # **1️⃣ Lógica de INICIO DE SESIÓN**
        if form_type == 'login':
            cedula = request.form.get('cedula')
            password = request.form.get('password')

            user = Dueño.query.filter_by(cedula=cedula).first()

            if user and user.check_password(password):
                login_user(user)
                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for('index'))  # Redirigir a la página principal
            else:
                flash("Cédula o contraseña incorrecta", "error")

        # **2️⃣ Lógica de REGISTRO**
        elif form_type == 'register':
            cedula_reg = request.form.get('cedula_reg')
            nombre_reg = request.form.get('nombre_reg')
            correo_reg = request.form.get('correo_reg')
            telefono_reg = request.form.get('telefono_reg')
            password_reg = request.form.get('password_reg')
            rol_reg = request.form.get('rol_reg')

            # Verificar si la cédula ya está registrada
            if Dueño.query.filter_by(cedula=cedula_reg).first():
                flash("Ya existe un dueño con esta cédula", "error")
            else:
                # Crear nuevo usuario Dueño
                nuevo_dueño = Dueño(
                    cedula=cedula_reg,
                    nombre=nombre_reg,
                    correo=correo_reg,
                    telefono=telefono_reg,
                    rol=rol_reg
                )
                # Utilizamos el método set_password para guardar la contraseña encriptada
                nuevo_dueño.set_password(password_reg)

                # Opcional: si el rol es 'admin', marcamos is_admin como True
                if rol_reg.lower() == "admin":
                    nuevo_dueño.is_admin = True

                db.session.add(nuevo_dueño)
                db.session.commit()

                login_user(nuevo_dueño)  # Iniciar sesión automáticamente después del registro
                flash("Registro exitoso, bienvenido", "success")
                return redirect(url_for('index'))  # Redirigir a la página principal

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "success")
    return redirect(url_for('index'))

@app.route('/admin/veterinarios')
@login_required
def admin_panel():
    if not current_user.is_admin_user():
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    # Obtener los veterinarios, dueños y mascotas desde la base de datos
    veterinarios = Veterinario.query.all()
    duenos = Dueño.query.all()
    mascotas = Mascota.query.all()

    return render_template('admin_panel.html', veterinarios=veterinarios, duenos=duenos, mascotas=mascotas)


@app.route('/admin/agregar_veterinario', methods=['GET', 'POST'])
@login_required
def agregar_veterinario():
    if not current_user.is_admin_user():
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        nuevo_veterinario = Veterinario(nombre=nombre)
        db.session.add(nuevo_veterinario)
        db.session.commit()
        flash("Veterinario agregado exitosamente", "success")
        return redirect(url_for('admin_panel'))

    return render_template('agregar_veterinario.html')


@app.route('/admin/editar_veterinario/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_veterinario(id):
    if not current_user.is_admin_user():
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    veterinario = Veterinario.query.get_or_404(id)

    if request.method == 'POST':
        # Obtener el nombre desde el formulario
        veterinario.nombre = request.form.get('nombre')
        
        # Guardar los cambios en la base de datos
        db.session.commit()

        flash("Veterinario actualizado exitosamente", "success")
        return redirect(url_for('admin_panel'))

    return render_template('editar_veterinario.html', veterinario=veterinario)



@app.route('/admin/eliminar_veterinario/<int:id>')
@login_required
def eliminar_veterinario(id):
    if not current_user.is_admin_user():
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for('index'))

    veterinario = Veterinario.query.get_or_404(id)
    db.session.delete(veterinario)
    db.session.commit()
    flash("Veterinario eliminado exitosamente", "success")
    return redirect(url_for('admin_panel'))


# Inicializa la base de datos al inicio
with app.app_context():
    db.create_all()
    create_admin()  # u otra función que llames en este bloque


# Ejecución de la aplicación
if __name__ == '__main__':
    app.run(debug=True)
