from flask import render_template, request

from mycrypto.forms import MovimientoForm
from mycrypto.models import ListaMovimientos, CoinApi, Movimiento, DBManager, RUTA_DB

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

        if 'calculadora' in request.form:
            if formulario.validate():
                moneda_origen = request.form.get('from_currency')
                moneda_destino = request.form.get('to_currency')
                cantidad = request.form.get('form_quantity')

                coin_api = CoinApi()
                peticion = coin_api.peticion_api(moneda_origen, moneda_destino)
                tasa = peticion[2]

                cantidad_cambio = lista.calcular_cantidad_cambio(
                    cantidad, tasa)

                precio_unitario = lista.calcular_pu(cantidad, cantidad_cambio)

                return render_template('form_compra.html', form=formulario,
                                       ca=cantidad_cambio,
                                       pu=precio_unitario, blockControl=True)
            else:
                return render_template('form_compra.html', form=formulario)
        else:
            if formulario.validate():
                moneda_origen = request.form.get('from_currency')
                moneda_destino = request.form.get('to_currency')
                cantidad = request.form.get('form_quantity')

                fecha = lista.obtener_fecha_sis()

                hora = lista.obtener_hora_sis()

                coin_api = CoinApi()
                peticion = coin_api.peticion_api(moneda_origen, moneda_destino)
                tasa = peticion[2]

                cantidad_cambio = lista.calcular_cantidad_cambio(
                    cantidad, tasa)

                precio_unitario = lista.calcular_pu(cantidad, cantidad_cambio)

                mov_dict = {
                    'date': fecha,
                    'time': hora,
                    'from_currency': moneda_origen,
                    'form_quantity': cantidad,
                    'to_currency': moneda_destino,
                    'to_quantity': cantidad_cambio,
                    'unit_price': precio_unitario
                }

                movimiento = Movimiento(mov_dict)

                bd = DBManager(RUTA_DB)
                bd.guardarMovimiento(movimiento)
                lista.cargar_movimiento()

                return render_template('inicio.html', movs=lista.movimientos)
            else:
                return render_template('form_compra.html', form=formulario)


@app.route('/status')
def status():
    return render_template('estado.html')
