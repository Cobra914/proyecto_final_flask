from datetime import date, time

import requests

import sqlite3

RUTA_DB = 'mycrypto/data/movements.db'

APIKEY = '7418c736-092b-42a6-9272-e626a5885fd1'
SERVER = 'https://rest.coinapi.io'
ENDPOINT = '/v1/exchangerate'
RUTA_API = SERVER + ENDPOINT
HEADERS = {
    'X-CoinAPI-Key': APIKEY
}


class DBManager:
    '''
    Clase para interactuar con la base de datos.
    '''

    def __init__(self, ruta):
        self.ruta = ruta

    def consultarSQL(self, consulta):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()

        cursor.execute(consulta)

        datos = cursor.fetchall()

        self.registros = []
        nombres_columna = []

        for columna in cursor.description:
            nombres_columna.append(columna[0])

        for dato in datos:
            movimiento = {}
            indice = 0
            for nombre in nombres_columna:
                movimiento[nombre] = dato[indice]
                indice += 1
            self.registros.append(movimiento)

        conexion.close()

        return self.registros


class Movimiento:

    def __init__(self, dict_mov):

        lista_monedas = ['EUR', 'BTC', 'ETH', 'USDT',
                         'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB']
        self.errores = []

        fecha = dict_mov.get('date', '')
        hora = dict_mov.get('time', '')
        from_currency = dict_mov.get('from_currency', '')
        form_quantity = dict_mov.get('form_quantity', None)
        to_currency = dict_mov.get('to_currency', '')
        to_quantity = dict_mov.get('to_quantity', None)
        unit_price = dict_mov.get('unit_price')

        self.id = dict_mov.get('id', None)

        # Validación hora
        try:
            self.fecha = date.fromisoformat(fecha)
        except ValueError:
            self.fecha = None
            msj = f'La fecha {fecha} no es una fecha ISO 8601 válida.'
            self.errores.append(msj)
        except TypeError:
            self.fecha = None
            msj = f'La fecha {fecha} no es una cadena de texto.'
            self.errores.append(msj)
        except:
            self.fecha = None
            msj = f'Error desconocido con la fecha.'
            self.errores.append(msj)

        # Validación fecha
        try:
            self.hora = time.fromisoformat(hora)
        except ValueError:
            self.hora = None
            msj = f'La hora {hora} no es de tipo ISO válida.'

        # Validación from_currency
        if from_currency not in lista_monedas:
            msj = f'La moneda {from_currency} no es una moneda válida.'
            self.errores.append(msj)
            raise ValueError(msj)
        else:
            self.from_currency = from_currency

        # Validación form_quantity
        try:
            valor = float(form_quantity)
            if valor > 0:
                self.form_quantity = valor
            else:
                self.form_quantity = 0
                msj = f'La cantidad debe ser mayor que cero.'
                self.errores.append(msj)
        except ValueError:
            self.form_quantity = 0
            msj = f'La cantidad debe ser un número decimal.'
            self.errores.append(msj)

        # Validación to_currency
        if to_currency not in lista_monedas:
            msj = f'La moneda {to_currency} no es una moneda válida.'
            self.errores.append(msj)
            raise ValueError(msj)
        else:
            self.to_currency = to_currency

        # Validación to_quantity
        try:
            valor = float(to_quantity)
            if valor > 0:
                self.to_quantity = valor
            else:
                # TODO Se rompe al ingresar un numero negativo
                self.to_quantity = 0
                msj = f'La cantidad debe ser mayor que cero.'
                self.errores.append(msj)
        except ValueError:
            self.to_quantity = 0
            msj = f'La cantidad debe ser un número decimal.'
            self.errores.append(msj)

        # self.from_currency = from_currency
        # self.form_quantity = form_quantity
        # self.to_currency = to_currency
        # self.to_quantity = to_quantity
        self.unit_price = unit_price

    @property
    def obtener_unit_price(self):
        n1 = float(self.form_quantity)
        n2 = float(self.to_quantity)
        resultado = n1/n2
        return round(resultado, 4)


class ListaMovimientos:

    def __init__(self):
        try:
            self.cargar_movimiento()
        except:
            self.movimientos = []

    def cargar_movimiento(self):
        db = DBManager(RUTA_DB)
        sql = 'SELECT id, date, time, from_currency, form_quantity, to_currency, to_quantity, unit_price FROM movimientos'
        datos = db.consultarSQL(sql)

        self.movimientos = []
        for dato in datos:
            mov = Movimiento(dato)
            self.movimientos.append(mov)


class CoinApi:

    def __init__(self, ruta):
        self.ruta = ruta

    def peticion_api(self, from_currency, to_currency, form_quantity):
        '''
        Consulta CoinApi para obtener "time" y "rate" sobre las monedas pedidas. 
        '''
        url = self.ruta + '/' + from_currency + '/' + to_currency

        respuesta = requests.get(url, headers=HEADERS)

        if respuesta.status_code == 200:
            datos = respuesta.json()

            tasa = datos.get('rate', 0)
            # hora =
        else:
            pass

        cantidad_en_ = form_quantity*tasa
