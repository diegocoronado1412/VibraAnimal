from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class RegistroDueñoForm(FlaskForm):
    cedula = StringField('Cédula', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    correo = StringField('Correo', validators=[Email()])
    telefono = StringField('Telefono', validators=[DataRequired()])  # Asegúrate de tener este campo
    submit = SubmitField('Registrar')
