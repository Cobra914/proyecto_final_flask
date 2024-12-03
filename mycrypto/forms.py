from flask_wtf import FlaskForm

from wtforms import DecimalField, HiddenField, StringField, SubmitField

from wtforms.validators import data_required, number_range


class MovimientoForm(FlaskForm):
    id = HiddenField()
    from_currency = StringField('From_currency')
    form_quantity = DecimalField('form_quantity', validators=[
        data_required(
            'Debes escribir una cantidad.'),
        number_range(
            min=0.1, message='No se permiten cantidades inferiores a 10 céntimos.')])
