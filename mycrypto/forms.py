from flask_wtf import FlaskForm

from wtforms import (DecimalField,
                     HiddenField, SelectField,
                     StringField,
                     SubmitField, ValidationError)

from wtforms.validators import data_required, number_range

lista_monedas = ['EUR', 'BTC', 'ETH', 'USDT',
                 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB']


class MovimientoForm(FlaskForm):
    from_currency = SelectField('De', choices=[('EUR', 'EUR'),
                                               ('BTC', 'BTC'),
                                               ('ETH', 'ETH'),
                                               ('USDT', 'USDT'),
                                               ('ADA', 'ADA'),
                                               ('SOL', 'SOL'),
                                               ('XRP', 'XRP'),
                                               ('DOT', 'DOT'),
                                               ('DOGE', 'DOGE'),
                                               ('SHIB', 'SHIB')])

    to_currency = SelectField('A', choices=[('EUR', 'EUR'),
                                            ('BTC', 'BTC'),
                                            ('ETH', 'ETH'),
                                            ('USDT', 'USDT'),
                                            ('ADA', 'ADA'),
                                            ('SOL', 'SOL'),
                                            ('XRP', 'XRP'),
                                            ('DOT', 'DOT'),
                                            ('DOGE', 'DOGE'),
                                            ('SHIB', 'SHIB')])

    form_quantity = DecimalField('C', validators=[
        data_required(
            'Debes escribir una cantidad.'),
        number_range(
            min=0.1, message='No se permiten cantidades inferiores a 10 céntimos.')])

    # calculadora = SubmitField('calculadora')
    # submit = SubmitField('guardar')

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
