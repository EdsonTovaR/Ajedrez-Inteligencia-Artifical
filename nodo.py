import chess


class Nodo(object):

    def __init__(self, movimiento=None, valor=None, tablero=None):
        self.tablero = tablero
        self.movimiento = movimiento
        self.valor = valor

    def __gt__(self, nodo):
        return self.valor > nodo.valor
