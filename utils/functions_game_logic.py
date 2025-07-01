import random
import pygame

MINA = -1
CUBIERTA = 0
DESCUBIERTA = 1
BANDERA = 2

def generar_matriz(filas, columnas, minas, primera_celda):
    matriz = []
    for fila in range(filas):
        fila_actual = []
        for columna in range(columnas):
            fila_actual.append(0)
        matriz.append(fila_actual)

    colocar_minas(matriz, minas, primera_celda)
    calcular_numeros(matriz)
    return matriz


def colocar_minas(matriz, cantidad, primera_celda):
    filas = len(matriz)
    columnas = len(matriz[0])
    colocadas = 0

    while colocadas < cantidad:
        f = random.randint(0, filas - 1)
        c = random.randint(0, columnas - 1)

        if (f, c) != primera_celda and matriz[f][c] != MINA:
            matriz[f][c] = MINA
            colocadas += 1

def calcular_numeros(matriz):
    for f in range(len(matriz)):
        for c in range(len(matriz[0])):
            if matriz[f][c] == MINA:
                continue
            minas = contar_minas_adyacentes(matriz, f, c)
            matriz[f][c] = minas

def contar_minas_adyacentes(matriz, fila_actual, columna_actual):
    cantidad_minas = 0
    for desplazamiento_fila in [-1, 0, 1]:
        for desplazamiento_columna in [-1, 0, 1]:
            fila_vecina = fila_actual + desplazamiento_fila
            columna_vecina = columna_actual + desplazamiento_columna
            if 0 <= fila_vecina < len(matriz) and 0 <= columna_vecina < len(matriz[0]):
                if matriz[fila_vecina][columna_vecina] == MINA:
                    cantidad_minas += 1
    return cantidad_minas


def descubrir(matriz_estado, matriz_juego, fila_actual, columna_actual):
    if matriz_estado[fila_actual][columna_actual] in (DESCUBIERTA, BANDERA):
        return False  

    if matriz_juego[fila_actual][columna_actual] == MINA:
        matriz_estado[fila_actual][columna_actual] = DESCUBIERTA
        return True   

    matriz_estado[fila_actual][columna_actual] = DESCUBIERTA

    if matriz_juego[fila_actual][columna_actual] == 0:
        for desplazamiento_fila in [-1, 0, 1]:
            for desplazamiento_columna in [-1, 0, 1]:
                fila_vecina = fila_actual + desplazamiento_fila
                columna_vecina = columna_actual + desplazamiento_columna
                if 0 <= fila_vecina < len(matriz_juego) and 0 <= columna_vecina < len(matriz_juego[0]):
                    if matriz_estado[fila_vecina][columna_vecina] != DESCUBIERTA:
                        descubrir(matriz_estado, matriz_juego, fila_vecina, columna_vecina)

    return False  


def activar_sonido_derrota():
    pygame.mixer.music.stop()
    sonido_derrota = pygame.mixer.Sound("assets/sounds/sonido_derrota.mp3")
    pygame.mixer.music.set_volume(0.5)
    sonido_derrota.play()