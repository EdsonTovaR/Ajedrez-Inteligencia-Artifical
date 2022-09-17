import heuristicas as h
import nodo as n


# emula w*h+w*h.....
def valor_heuristicas(board):
    total_points = 0
    total_points += h.material(board, 50)
    total_points += h.estructura_peones(board, 10)
    total_points += h.jaque(board, 50)
    total_points += h.cuadrados(board, 50)
    return total_points


def greedy(board):
    mejor_movimiento = 0
    mejor_valor = -999
    for i in board.legal_moves:
        board.push(i)
        valores = valor_heuristicas(board)
        if valores > mejor_valor:
            mejor_movimiento = i
            mejor_valor = valores
        board.pop()
    return mejor_movimiento


def hacer_movimiento_m(board):
    posibles = genera_hijo(board)
    mejor_mov = n.Nodo("", -999)
    for mov in posibles:
        if mov.valor > mejor_mov.valor:
            mejor_mov = mov
    return mejor_mov.movimiento


def minimax(board, llamadas, current_depth=0, max_depth=4):
    current_depth += 1
    llamadas += 1

    if current_depth == max_depth:
        # valor heuristico
        valor = valor_heuristicas(board)
        return valor, None, llamadas

    if current_depth % 2 == 0:
        # Turno jugador minimo
        best = float('inf')
        mejor_mov = None
        for i in board.legal_moves:
            board.push(i)
            algo, algo2, llamadas = minimax(
                board, llamadas, current_depth, max_depth)
            board.pop()
            if algo < best:
                best = algo
                mejor_mov = i

        return best, mejor_mov, llamadas
    else:
        # Turno jugador maximo
        best = float('-inf')
        mejor_mov = None
        for i in board.legal_moves:
            board.push(i)
            algo, algo2, llamadas = minimax(
                board, llamadas, current_depth, max_depth)
            board.pop()
            if algo > best:
                best = algo
                mejor_mov = i
        return best, mejor_mov, llamadas


#########################################################################
def minimax_a_(board, llamadas, current_depth=0, max_depth=4):
    current_depth += 1
    llamadas += 1

    if current_depth == max_depth:
        # valor heuristico
        valor = valor_heuristicas(board)
        return valor, None, llamadas

    if current_depth % 2 == 0:
        # Turno jugador minimo
        best = float('inf')
        mejor_mov = None
        posibles = genera_hijo(board)
        for i in posibles:
            board.push(i.movimiento)
            algo, algo2, llamadas = minimax_a_(
                board, llamadas, current_depth, max_depth)
            board.pop()
            if algo < best:
                best = algo
                mejor_mov = i

        return best, mejor_mov, llamadas
    else:
        # Turno jugador maximo
        best = float('-inf')
        mejor_mov = None
        posibles = genera_hijo(board)
        for i in posibles:
            board.push(i.movimiento)
            algo, algo2, llamadas = minimax_a_(
                board, llamadas, current_depth, max_depth)
            board.pop()
            if algo > best:
                best = algo
                mejor_mov = i
        return best, mejor_mov, llamadas

##############################################################################


def ab_minimax(board, llamadas, current_depth=0, max_depth=4, alpha=float("-inf"), beta=float("inf")):
    current_depth += 1
    llamadas += 1
    if current_depth == max_depth:
        # Obtiene valor heuristicas
        valor = valor_heuristicas(board)
        return valor, None, llamadas

    if current_depth % 2 == 0:
        # Turno jugador minimo
        best = float('inf')
        best_move = None
        for i in board.legal_moves:
            board.push(i)
            algo, algo2, llamadas = ab_minimax(
                board, llamadas, current_depth, max_depth, alpha, beta)
            board.pop()
            beta = min(beta, algo)
            if algo < best:
                best = algo
                best_move = i
            if best < alpha:
                break
        return best, best_move, llamadas
    else:
        # Turno jugador maximo
        best = float('-inf')
        best_move = None
        for i in board.legal_moves:
            board.push(i)
            algo, algo2, llamadas = ab_minimax(
                board, llamadas, current_depth, max_depth, alpha, beta)
            board.pop()
            alpha = max(alpha, algo)
            if algo > best:
                best = algo
                best_move = i
            if best > beta:
                break
        return (best, best_move, llamadas)


######################################################################
def genera_hijo(lista):
    mov = []
    for i in lista.legal_moves:
        lista.push(i)
        valor = valor_heuristicas(lista)
        aux = n.Nodo(i, valor, lista.fen())
        mov.append(aux)
        lista.pop()
    return mov
