from datetime import date, time


RUTA_DB = 'mycrypto/data/movements.db'


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
