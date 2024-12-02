from flask import render_template

from mycrypto.models import ListaMovimientos

from . import app


@app.route('/')
def home():
    lista = ListaMovimientos()
    if lista.movimientos != []:
        return render_template('inicio.html', movs=lista.movimientos)
    else:
        return render_template('sin_movimientos.html')
