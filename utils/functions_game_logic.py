import random
import pygame


def generar_matriz(filas, columnas, minas, primera_celda, MINA):
    """
    Genera la matriz del buscaminas con las minas ubicadas y los números correspondientes.
    Recibe la cantidad de filas, columnas, cantidad de minas y la primera celda clickeada.
    Devuelve la matriz completa con minas y números generados.
    """
    matriz = []
    for fila in range(filas):
        fila_actual = []
        for columna in range(columnas):
            fila_actual.append(0)
        matriz.append(fila_actual)

    colocar_minas(matriz, minas, primera_celda, MINA)
    calcular_numeros(matriz, MINA)
    return matriz


def colocar_minas(matriz, cantidad, primera_celda, MINA):
    """
    Ubica aleatoriamente las minas en la matriz.
    Recibe la matriz, la cantidad de minas a colocar y la posición de la primera celda (para evitar poner mina allí).
    No retorna nada, modifica la matriz en el lugar.
    """
    filas = len(matriz)
    columnas = len(matriz[0])
    colocadas = 0

    while colocadas < cantidad:
        f = random.randint(0, filas - 1)
        c = random.randint(0, columnas - 1)

        if (f, c) != primera_celda and matriz[f][c] != MINA:
            matriz[f][c] = MINA
            colocadas += 1


def calcular_numeros(matriz, MINA):
    """
    Calcula los números de cada celda en función de las minas adyacentes.
    Recibe la matriz y la modifica directamente.
    No retorna nada.
    """
    for f in range(len(matriz)):
        for c in range(len(matriz[0])):
            if matriz[f][c] == MINA:
                continue
            minas = contar_minas_adyacentes(matriz, f, c, MINA)
            matriz[f][c] = minas


def contar_minas_adyacentes(matriz, fila_actual, columna_actual, MINA):
    """
    Cuenta cuántas minas rodean a una celda.
    Recibe la matriz, la fila y la columna de la celda a evaluar.
    Devuelve la cantidad de minas adyacentes como entero.
    """
    cantidad_minas = 0
    for desplazamiento_fila in [-1, 0, 1]:
        for desplazamiento_columna in [-1, 0, 1]:
            fila_vecina = fila_actual + desplazamiento_fila
            columna_vecina = columna_actual + desplazamiento_columna
            if 0 <= fila_vecina < len(matriz) and 0 <= columna_vecina < len(matriz[0]):
                if matriz[fila_vecina][columna_vecina] == MINA:
                    cantidad_minas += 1
    return cantidad_minas


def descubrir(matriz_estado, matriz_juego, fila_actual, columna_actual, estados):
    """
    Destapa una celda. Si es cero, destapa también en forma recursiva las celdas vecinas.
    Recibe la matriz de estados (cubierta/descubierta), la matriz de juego (minas/números) y la posición de la celda.
    Devuelve True si se descubrió una mina, False en caso contrario.
    """
    MINA = estados[0]
    DESCUBIERTA = estados[1]
    BANDERA = estados[2]

    if matriz_estado[fila_actual][columna_actual] == DESCUBIERTA or matriz_estado[fila_actual][columna_actual] == BANDERA:
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
                        descubrir(matriz_estado, matriz_juego, fila_vecina, columna_vecina, (MINA, DESCUBIERTA, BANDERA))

    return False  


def activar_sonido_derrota():
    """
    Detiene la música de fondo y reproduce el sonido de derrota.
    No recibe parámetros ni devuelve nada.
    """
    pygame.mixer.music.stop()
    sonido_derrota = pygame.mixer.Sound("assets/sounds/sonido_derrota.mp3")
    pygame.mixer.music.set_volume(0.5)
    sonido_derrota.play()
