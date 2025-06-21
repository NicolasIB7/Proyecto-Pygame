import pygame
from funciones import *

pygame.init()

ANCHO_PANTALLA = 800  # X
ALTO_PANTALLA = 600  # Y
#               R    G    B
COLOR_FONDO = (102, 233, 237)
COLOR_BOTON = (245, 153, 49)
COLOR_BORDE = (23, 23, 22)
COLOR_TEXTO = (138, 14, 0)


# Sonidos
# Musica de fondo
ruta_sonido = "sonido_fondo.mp3"
pygame.mixer.music.load(ruta_sonido)
pygame.mixer.music.set_volume(0.5)  # 0 (0%) - 1 (100%)
bandera_musica_fondo = False


pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Buscaminas - MARIO BROS")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)


# Texto por pantalla
fuente = pygame.font.SysFont("Arial", 24)
fuente_encabezado = pygame.font.SysFont("Arial", 20, bold=True)


pantalla_principal = False
pantalla_puntajes = True


# ----------------------------------------------------------------------#


config_puntajes = obtener_config_puntajes(
    pygame, pantalla, ANCHO_PANTALLA, ALTO_PANTALLA)


corriendo = True
while corriendo:
    if pantalla_principal == True:
        if bandera_musica_fondo:
            pygame.mixer.music.stop()
            bandera_musica_fondo = False

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        pantalla.fill(COLOR_FONDO)

        pantalla.blit("texto_menu", (50, 50))

    if pantalla_puntajes == True:

        pantalla.fill(COLOR_FONDO)

        generar_texto_inicial(config_puntajes)
        lista_puntajes = leer_puntajes()
        generar_tabla_puntajes(pygame, lista_puntajes, config_puntajes)
        rect_boton_volver = generar_boton_volver(pygame, config_puntajes)

        # sonido
        if bandera_musica_fondo == False:
            pygame.mixer.music.play(-1)
            bandera_musica_fondo = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            # boton volver
            if evento.type == pygame.MOUSEBUTTONDOWN:

                if rect_boton_volver.collidepoint(evento.pos) == True:
                    if evento.button == 1:  # Boton izquierdo
                        pantalla_puntajes = False
                        pantalla_principal = True
            # volver con ESC
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pantalla_puntajes = False
                    pantalla_principal = True

    pygame.display.flip()  # Actualiza TODA la pantalla del juego
