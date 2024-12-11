from flask_wtf import FlaskForm

from wtforms import (DecimalField,
                     HiddenField,
                     StringField,
                     SubmitField, ValidationError)

from wtforms.validators import data_required, number_range

lista_monedas = ['EUR', 'BTC', 'ETH', 'USDT',
                 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB']


class MovimientoForm(FlaskForm):
    id = HiddenField()
    from_currency = StringField('From_currency')
    to_currency = StringField('To_currency')
    form_quantity = DecimalField('Form_quantity', validators=[
        data_required(
            'Debes escribir una cantidad.'),
        number_range(
            min=0.1, message='No se permiten cantidades inferiores a 10 céntimos.')])

    calculadora = SubmitField('Calculadora')
    submit = SubmitField('Guardar')

    def validate_from_currency(form, field):

        if field.data not in lista_monedas:
            raise ValidationError(
                'La moneda no existe o no está entre las 10 monedas de la app.')
        else:
            pass

    def validate_to_currency(form, field):

        if field.data not in lista_monedas:
            raise ValidationError(
                'La moneda no existe o no está entre las 10 monedas de la app.')
