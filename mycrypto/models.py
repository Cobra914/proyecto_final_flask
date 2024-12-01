from datetime import date, time

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


class Movimiento:

    def __init__(self, dict_mov):

        self.errores = []

        fecha = dict_mov.get('date', '')
        hora = dict_mov.get('time', '')
        from_currency = dict_mov.get('from_currency', '')
        form_quantity = dict_mov.get('form_quantity', None)
        to_currency = dict_mov.get('to_currency', '')
        to_quantity = dict_mov.get('to_quantity', None)

        self.id = dict_mov.get('id', None)

        try:
            self.fecha = date.fromisoformat(fecha)
        except ValueError:
            self.fecha = None
            msj = f'La fecha {fecha} no es una fecha ISO 8601 válida'
            self.errores.append(msj)
        except TypeError:
            self.fecha = None
            msj = f'La fecha {fecha} no es una cadena de texto'
            self.errores.append(msj)
        except:
            self.fecha = None
            msj = f'Error desconocido con la fecha'
            self.errores.append(msj)

        try:
            self.hora = time.fromisoformat(hora)
        except ValueError:
            self.hora = None
            msj = f'La hora {hora} no es de tipo ISO válida'

        self.from_currency = from_currency
        self.form_quantity = form_quantity
        self.to_currency = to_currency
        self.to_quantity = to_quantity


class ListaMovimientos:

    def __init__(self):
        try:
            self.cargar_movimiento()
        except:
            self.movimientos = []

    def cargar_movimiento(self):
        db = DBManager(RUTA_DB)
        sql = 'SELECT id, date, time, from_currency, form_quantity, to_currency, to_quantity FROM movimientos'
        datos = db.consultarSQL(sql)

        self.movimientos = []
        for dato in datos:
            mov = Movimiento(dato)
            self.movimientos.append(mov)
