from mycrypto import app

from datetime import datetime, date, time

import pytz

import requests

import sqlite3

RUTA_DB = 'mycrypto/data/movements.db'


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

    def guardarMovimiento(self, movimiento):
        '''
        Agrega el movimiento a la lista en la BD.
        '''
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        sql = 'INSERT INTO movimientos ("date", "time", "from_currency", "form_quantity", "to_currency", "to_quantity", "unit_price") VALUES (?, ?, ?, ?, ?, ?, ?)'

        try:
            params = (
                movimiento.date,
                str(movimiento.time),
                movimiento.from_currency,
                movimiento.form_quantity,
                movimiento.to_currency,
                movimiento.to_quantity,
                movimiento.unit_price
            )
            cursor.execute(sql, params)
            conexion.commit()
        except Exception as ex:
            print(ex)
            conexion.rollback()

        conexion.close()


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
        unit_price = dict_mov.get('unit_price', None)

        self.id = dict_mov.get('id', None)

        # Validación fecha
        try:
            self.date = date.fromisoformat(fecha)
        except ValueError:
            self.date = None
            msj = f'La fecha {fecha} no es una fecha ISO 8601 válida.'
            self.errores.append(msj)
        except TypeError:
            self.date = None
            msj = f'La fecha {fecha} no es una cadena de texto.'
            self.errores.append(msj)
        except:
            self.date = None
            msj = f'Error desconocido con la fecha.'
            self.errores.append(msj)

        # Validación hora
        # self.time = hora
        try:
            self.time = time.fromisoformat(hora)
        except TypeError:
            self.time = None
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
                msj = 'La cantidad debe ser mayor que cero.'
                self.errores.append(msj)
        except ValueError:
            self.form_quantity = 0
            msj = 'La cantidad debe ser un número entero o decimal positivo.'
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
                self.to_quantity = 0
                msj = 'La cantidad debe ser mayor que cero.'
                self.errores.append(msj)
        except ValueError:
            self.to_quantity = 0
            msj = 'La cantidad debe ser un número entero o decimal positivo.'
            self.errores.append(msj)

        # Validación unit_price
        try:
            valor = float(unit_price)
            if valor > 0:
                valor = "{:.6f}".format(valor)
                self.unit_price = valor
            else:
                self.unit_price = 0
                msj = 'Error en el cálculo del precio unitario.'
                self.errores.append(msj)
        except ValueError:
            self.unit_price = 0
            msj = 'La cantidad debe ser un número entero o decimal positivo.'
            self.errores.append(msj)

    def __str__(self):
        return f'{self.date} | {self.time} | {self.from_currency} | {self.form_quantity} | {self.to_currency} | {self.to_quantity} | {self.unit_price}'

    def __repr__(self):
        return self.__str__()


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

    def peticion_api(self, from_currency, to_currency):
        '''
        Consulta CoinApi para obtener "time" y "rate" sobre las monedas pedidas.
        '''
        SERVER = 'https://rest.coinapi.io'
        ENDPOINT = '/v1/exchangerate'
        HEADERS = {
            'X-CoinAPI-Key': app.config['API_KEY']
        }

        url = SERVER + ENDPOINT + '/' + from_currency + '/' + to_currency

        respuesta = requests.get(url, headers=HEADERS)

        lista_datos = []

        if respuesta.status_code == 200:
            datos = respuesta.json()

            fecha_hora_str = datos.get('time', '')

            fecha_hora_obj = datetime.fromisoformat(fecha_hora_str.rstrip('Z'))
            fecha_hora_obj = fecha_hora_obj.replace(tzinfo=pytz.UTC)
            fecha_hora_local = fecha_hora_obj.astimezone(
                pytz.timezone('Europe/Madrid'))

            fecha_obj = fecha_hora_local.date()
            fecha_iso_str = fecha_obj.isoformat()
            lista_datos.append(fecha_iso_str)

            hora_obj = fecha_hora_local.time()
            hora_iso_str = hora_obj.isoformat()
            lista_datos.append(hora_iso_str)

            tasa = datos.get('rate', 0)
            lista_datos.append(tasa)
        elif respuesta.status_code == 401:
            raise ValueError(
                'API key inválida')
        elif respuesta.status_code == 403:
            raise MiError(
                'La API key carece de permisos para obtener la información pedida')
        elif respuesta.status_code == 429:
            raise MiError(
                'Se ha agotado la cantidad de solicitudes a CoinApi')
        else:
            raise MiError('Error desconocido')

        return lista_datos


class MiError(Exception):
    pass
