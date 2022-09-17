
import copy
import math
import random


class Node:

    def __init__(self, movimiento=None, parent=None, estado=None, board=None):
        self.movimiento = movimiento
        self.nodoPadre = parent
        self.nodosHijos = []
        self.victorias = 0
        self.visitas = 0
        self.movimientosNoIntentados = list(board.legal_moves)
        self.turnoJugador = board.turn

        # retonar el mayor
    def UCTseleccionarHijo(self):
        s = sorted(self.nodosHijos, key=lambda c: c.victorias / c.visitas +
                   math.sqrt(2 * math.log(self.visitas) / c.visitas))[-1]
        return s

    def AnadirHijo(self, m, s, board):
        n = Node(movimiento=m, parent=self, estado=s, board=board)
        self.movimientosNoIntentados.remove(m)
        self.nodosHijos.append(n)
        return n

    def Actualizar(self, result):
        self.visitas += 1
        self.victorias += result


def UCT(estadobase, itermax, board):
    rootnode = Node(estado=estadobase, board=board)

    for i in range(itermax):
        node = rootnode
        # estado es una copia del tablero
        estado = copy.deepcopy(estadobase)

        # Select
        while node.movimientosNoIntentados == [] and node.nodosHijos != []:
            node = node.UCTseleccionarHijo()
            estado.push(node.movimiento)

        # Expand
        if node.movimientosNoIntentados != []:
            m = random.choice(node.movimientosNoIntentados)
            estado.push(m)
            node = node.AnadirHijo(m, estado, board)

        # rollout
        # while estado is non-terminal
        while not estado.is_game_over()and list(estado.legal_moves) != []:
            estado.push(random.choice(list(estado.legal_moves)))

        # Backpropagate
        while node is not None:
            node.Actualizar(resultados(estado))
            node = node.nodoPadre

    return sorted(rootnode.nodosHijos, key=lambda c: c.visitas)[-1].movimiento


def resultados(board):
    var = str(board.result())
    if(var == "1/2-1/2"):
        return 1
    elif (var == "1-0"):
        return 0
    elif (var == "0-1"):
        return 2
    else:
        return 1
