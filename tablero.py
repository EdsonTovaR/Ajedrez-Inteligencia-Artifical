import chess
import funciones as f


print("seleccione un algortimo para ejecutar la IA")
for element in f.algoritmos:
    print(element, f.algoritmos[element])
print("7", "competencia")

print("Ingrese el numero correspondiente")
clave = int(input())
board = chess.Board()
if(clave == 7):
    f.juego(board, "competencia")
else:
    f.juego(board, f.algoritmos[clave])
