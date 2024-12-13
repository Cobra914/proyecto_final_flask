from flask import render_template, request

from mycrypto.forms import MovimientoForm
from mycrypto.models import ListaMovimientos, CoinApi

from . import app


@app.route('/')
def home():
    lista = ListaMovimientos()
    return render_template('inicio.html', movs=lista.movimientos)


@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'GET':
        formulario = MovimientoForm()
        return render_template('form_compra.html', form=formulario)

    if request.method == 'POST':
        lista = ListaMovimientos()
        formulario = MovimientoForm(data=request.form)

        # print('---------------------------------')
        # print(request.form)
        # print('---------------------------------')

        if 'calculadora' in request.form:
            if formulario.validate():
                moneda_origen = request.form.get('from_currency')
                moneda_destino = request.form.get('to_currency')

                coin_api = CoinApi()
                peticion = coin_api.peticion_api(moneda_origen, moneda_destino)

                cantidad = request.form.get('form_quantity')
                cantidad = float(cantidad)
                tasa = peticion[2]
                cantidad_cambio = cantidad*tasa
                precio_unitario = cantidad/cantidad_cambio

                return render_template('form_compra.html', form=formulario, ca=cantidad_cambio, pu=precio_unitario)
            else:
                return render_template('form_compra.html', form=formulario)
        else:
            pass
        # return 'guardar'
        return render_template('inicio.html')


@app.route('/status')
def status():
    return render_template('estado.html')
