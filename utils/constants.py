
import pygame
from utils.functions_game_menu import *

# Dimensiones
ANCHO=800
ALTO =600

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


colores_numeros = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128)
}

fondo_pantall_juego = pygame.image.load(
    'assets/images/fondo_pantalla_juego.jpg')
fondo_pantall_juego = pygame.transform.scale(
    fondo_pantall_juego, (ANCHO, ALTO))


# diccionarios de los elementos

dic_buscaminas = [{'dimension': 0.95, 'x': 0.55, 'y': 0.05}]

dic_botones = [
    {'ancho': 0.19, 'alto': 0.14, 'x': 0.06, 'y': 0.80,
        'texto': 'assets/images/texto_volver.png', 'fondo': 'assets/images/fondo_boton.png'},
    {'ancho': 0.19, 'alto': 0.14, 'x': 0.06, 'y': 0.62,
        'texto': 'assets/images/texto_pausar.png', 'fondo': 'assets/images/fondo_boton.png'},
    {'ancho': 0.12, 'alto': 0.16, 'x': 0.09, 'y': 0.44,
        'texto': 'assets/images/honguito_verde.png', 'fondo': 'assets/images/fondo_boton.png'}
]

dic_contador = [{'ancho': 0.14, 'alto': 0.14,
                 'x': 0.082, 'y': 0.25, 'fuente': 0.65}]

dic_timer = [
    {'ancho': 0.22, 'alto': 0.15, 'x': 0.04, 'y': 0.05,
        'texto': [0, 0], 'color': (255, 0, 0), 'fuente': 80}
]

dic_botones_dif = [
    {'ancho': 0.22, 'alto': 0.26, 'x': 0.10, 'y': 0.60, 'texto': 'assets/images/boton_facil.png',
        'fondo': 'assets/images/fondo_boton_dificultad.png'},
    {'ancho': 0.22, 'alto': 0.26, 'x': 0.40, 'y': 0.60, 'texto': 'assets/images/boton_normal.png',
        'fondo': 'assets/images/fondo_boton_dificultad.png'},
    {'ancho': 0.22, 'alto': 0.26, 'x': 0.70, 'y': 0.60, 'texto': 'assets/images/boton_dificil.png',
        'fondo': 'assets/images/fondo_boton_dificultad.png'}
]

dic_valores_dif = [
    {'dificultad': 'facil', 'columnas': 8, 'minas': 10},
    {'dificultad': 'normal', 'columnas': 16, 'minas': 50},
    {'dificultad': 'dificil', 'columnas': 24, 'minas': 120}
]


# pantalla dificultad
imagenes_hover = ['assets/images/texto_volver_hover.png',
                  'assets/images/texto_pausar_hover.png', 'assets/images/honguito_rojo.png']
img_dif_hover = ['assets/images/boton_facil_hover.png',
                 'assets/images/boton_normal_hover.png', 'assets/images/boton_dificil_hover.png']
