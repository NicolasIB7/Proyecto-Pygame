import pygame

# Dimensiones
ANCHO, ALTO = 800, 600

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 120, 255)
BLANCO = (255, 255, 255)
COLOR_TEXTO_BOTONES = (255, 255, 255)
COLOR_CELDA_OCULTA = (134, 47, 16)
COLOR_CELDA_MARCO = (64, 21, 5)
COLOR_TIMER_NUMEROS = (255, 0, 0)
COLOR_FONDO = (34, 139, 27)
COLOR_RECTANGULOS = (0, 0, 0)
COLOR_DESCUBIERTA = (192, 192, 192)  

# Cuadro Buscaminas
ancho_buscaminas = ANCHO * 0.65
alto_buscaminas = ALTO * 0.85
posicion_x_buscaminas = ANCHO * 0.3
posicion_y_buscaminas = ALTO * 0.08


# Filas x Columnas 
FILAS = 8
COLUMNAS = 8
tamaño_celda = int(ancho_buscaminas / COLUMNAS)

# Rectángulo principal del juego
rec_buscaminas = pygame.Rect(
    posicion_x_buscaminas, posicion_y_buscaminas, ancho_buscaminas, alto_buscaminas)

# Botones
ancho_boton = ANCHO * 0.19
alto_boton = ALTO * 0.14
posicion_x_boton = ANCHO * 0.06
posicion_y_boton = ALTO * 0.75

rec_boton_volver = pygame.Rect(posicion_x_boton, posicion_y_boton, ancho_boton, alto_boton)
rec_boton_reiniciar = pygame.Rect(posicion_x_boton, posicion_y_boton - 200, ancho_boton, alto_boton)
rec_boton_pausar = pygame.Rect(posicion_x_boton, posicion_y_boton - 100, ancho_boton, alto_boton)

# Timer
ancho_cuadro_timer = ANCHO * 0.25
alto_cuadro_timer = ALTO * 0.15
posicion_x_timer = ANCHO * 0.03
posicion_y_timer = ALTO * 0.05

cuadro_timer = pygame.Rect(posicion_x_timer, posicion_y_timer, ancho_cuadro_timer, alto_cuadro_timer)