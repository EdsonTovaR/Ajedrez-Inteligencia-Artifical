import algoritmos as algo
import chess
import heuristicas as h
import mcts as no
import nodo as n
import os
import time


sleepy = 0
algoritmos = {
    1: "greedy_p",
    2: "greedy_o",
    3: "minimax_p",
    4: "minimax_o",
    5: "ab_minimax_p",
    6: "mcts",
}


class SortedDisplayDict(dict):

    def __str__(self):
        return "{" + ", ".join("%r: %r" % (key, self[key]) for key in sorted(self)) + "}"


piezas_comidas_blancas, piezas_actuales_negras = {}, {}
iteraciones = [500, 750, 1000, 1250]
profundidades = [4, 5, 6, 7]


def escribir_fichero(texto, archivo):
    F = open(archivo, "a")
    F.write(texto)
    F.write("\n")
    F.close()


def piezas_comidas(board):
    piezas_actuales_blancas, piezas_actuales_negras = h.contar_piezas(board)
    piezas_comidas_blancas = {key: h.totales_blancas[
        key] - piezas_actuales_blancas.get(key, 0) for key in h.totales_blancas}
    piezas_comidas_negras = {key: h.totales_negras[
        key] - piezas_actuales_negras.get(key, 0) for key in h.totales_negras}
    return (piezas_comidas_blancas, piezas_comidas_negras)


def marcador(board):
    blancas, negras = piezas_comidas(board)
    blancas = SortedDisplayDict(blancas)
    negras = SortedDisplayDict(negras)
    print("capturadas x blancas", negras)
    print("capturadas x negras ", blancas)


def validar(mov):
    return 'a' <= mov[0] <= 'h' and '1' <= mov[1] <= '8' and 'a' <= mov[2] <= 'h' and '1' <= mov[3] <= '8'


def mensaje_impreso(a1, a2, board, prueba):
    if prueba:
        porcentaje = a1 / a2 * 100
        palabra1 = "Se han recorrido " + \
            str(a1) + " de Nodos con alpha-beta en turno " + \
            str(board.fullmove_number)
        palabra2 = "Se han recorrido " + \
            str(a2) + " de Nodos minimax en turno " + \
            str(board.fullmove_number)
        palabra3 = "Se ha reducido en un " + \
            str(porcentaje) + "%" + " la busqueda del mov"
        palabra = palabra1 + "\n" + palabra2 + "\n" + palabra3
        escribir_fichero(palabra, "salida.txt")


def juego(board, algoritmo, prueba=False):
    os.system('cls')
    tiempo = 0
    if(algoritmo != "competencia"):
        while(not board.is_game_over()):
            print("turno numero: " + str(board.fullmove_number))
            if(tiempo):
                print("Tiempo tomado en calcular respuesta: ", tiempo)
            turno_jugador(board, prueba)

            if not board.is_game_over():
                print("Turno Computador....")
                tiempo = turno_ia(board, algoritmo, prueba)
                os.system('cls')
            else:
                break
    else:
        print("seleccione los algoritmos para ejecutar")
        for element in algoritmos:
            print(element, algoritmos[element])
        clave = int(input())
        clave1 = int(input())
        while(not board.is_game_over()):
            print("turno numero: " + str(board.fullmove_number))
            marcador(board)
            print(board)
            if(tiempo and tiempo1):
                print("IA1", tiempo)
                print("IA2", tiempo1)
            tiempo = turno_ia(board, algoritmos[clave], prueba)
            tiempo1 = turno_ia(board, algoritmos[clave1], prueba)
            time.sleep(sleepy)
            os.system('cls')

    var = str(board.result())
    if (var == "1-0"):
        print("Gana las Blancas")
    elif (var == "0-1"):
        print("Gana las Negras")
    else:
        print("Empate")


# problema con el turno del jugador si el string no es de tam 4
def turno_jugador(board, prueba):
    print("Turno jugador....")
    if prueba:
        board.push(algo.greedy(board))
        return
    marcador(board)
    print(board)
    entrada = input()
    while(entrada):

        if entrada == 'v':
            print(board)

        elif entrada == 'h' or entrada == 'H':
            print("Mov disponibles " + str(board.legal_moves.count()))
            for i in board.legal_moves:
                print(str(board.piece_at(i.from_square)) + ' : ' + board.uci(i))

        elif(len(entrada) == 4 and validar(entrada)):
            mov = chess.Move.from_uci(entrada)
            if mov in board.legal_moves:
                board.push(mov)
                del mov
                break
            print("movimiento invalido intente nuevamente")
        entrada = input()
    return False


def turno_ia(board, algoritmo, prueba, llamadas=0, llam=0):

    if algoritmo == "greedy_p":
        print("greedy_p")
        inicio = time.time()
        mov = algo.greedy(board)
        final = time.time()
        tiempo = final - inicio
        # escribir_fichero(str(tiempo), "tiempos.txt")
        # print("tiempo tomado ", tiempo)
        board.push(mov)
        del mov

    elif algoritmo == "greedy_o":
        print("greedy_o")
        inicio = time.time()
        mov = algo.hacer_movimiento_m(board)
        final = time.time()
        tiempo = final - inicio
        # escribir_fichero(str(tiempo), "tiempos.txt")
        # print("tiempo tomado ", tiempo)
        board.push(mov)
        del mov

    elif algoritmo == "minimax_p":
        if not prueba:
            print("minimax_p")
            inicio = time.time()
            valor, mov, llam = algo.minimax(board, llam)
            final = time.time()
            tiempo = final - inicio
            # escribir_fichero(str(tiempo), "tiempos.txt")
            # print(valor)
            board.push(mov)
            del mov
        else:
            for ite in profundidades:
                print("minimax_p")
                inicio = time.time()
                valor, mov, llam = algo.minimax(board, llam, max_depth=ite)
                final = time.time()
                tiempo = final - inicio
                # escribir_fichero(str(ite) + ' ' + str(tiempo), "tiempos.txt")
            board.push(mov)
            del mov

    elif algoritmo == "ab_minimax_p":
        if not prueba:
            print("ab_minimax_p")
            inicio = time.time()
            valor, mov, llamadas = algo.ab_minimax(board, llamadas)
            final = time.time()
            tiempo = final - inicio
            # escribir_fichero(str(tiempo), "tiempos.txt")
            # mensaje_impreso(llamadas, llam, board, prueba)
            board.push(mov)
            del mov
        else:
            for ite in profundidades:
                print("ab_minimax_p")
                inicio = time.time()
                valor, mov, llamadas = algo.minimax(
                    board, llamadas, max_depth=ite)
                final = time.time()
                tiempo = final - inicio
                # escribir_fichero(str(ite) + ' ' + str(tiempo), "tiempos.txt")
            board.push(mov)
            del mov

    elif algoritmo == "minimax_o":
        print("minimax_o")
        inicio = time.time()
        valor, mov, llamadas = algo.minimax_a_(board, 0)
        final = time.time()
        tiempo = final - inicio
        # escribir_fichero(str(tiempo), "tiempos.txt")
        board.push(mov.movimiento)
        del mov

    elif algoritmo == "mcts":
        if not prueba:
            print("mcts")
            inicio = time.time()
            mov = no.UCT(estadobase=board, itermax=500, board=board)
            final = time.time()
            tiempo = final - inicio
            # escribir_fichero(str(tiempo), "tiempos.txt")
            print(tiempo)
            board.push(mov)
            del mov
        else:
            for ite in iteraciones:
                print("mcts")
                inicio = time.time()
                mov = no.UCT(estadobase=board, itermax=ite, board=board)
                final = time.time()
                tiempo = final - inicio
                # escribir_fichero(str(tiempo), "tiempos.txt")
    return tiempo
