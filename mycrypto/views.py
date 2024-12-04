from flask import render_template

from mycrypto.models import ListaMovimientos

from . import app


@app.route('/')
def home():
    lista = ListaMovimientos()
    return render_template('inicio.html', movs=lista.movimientos)


@app.route('/purchase')
def purchase():
    return render_template('compra.html')


@app.route('/status')
def status():
    return render_template('estado.html')
