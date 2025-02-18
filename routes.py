from flask import render_template, redirect, url_for
from main import app, db
from models_veterinaria import Dueño
from forms import RegistroDueñoForm

@app.route('/registro_dueno', methods=['GET', 'POST'])
def registro_dueño():
    form = RegistroDueñoForm()
    if form.validate_on_submit():
        dueño = Dueño(cedula=form.cedula.data, nombre=form.nombre.data,
                      correo=form.correo.data, telefono=form.telefono.data)  # Cambio de 'celular' a 'telefono'
        db.session.add(dueño)
        db.session.commit()
        return redirect(url_for('home'))  # Redirige a la página de inicio
    return render_template('registro_dueno.html', form=form)
