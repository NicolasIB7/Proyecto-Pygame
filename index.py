import pygame

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


rect_boton = pygame.Rect(50, 50, 300, 100)

# Texto por pantalla
fuente = pygame.font.SysFont("Arial", 25)

texto_volver = fuente.render("Presione ESCAPE para volver.", True, COLOR_BORDE)
texto_menu = fuente.render("Estoy en el menú principal", True, COLOR_BORDE)

pantalla_principal = False
pantalla_puntajes = True


# ----------------------------------------------------------------------#

# TEXTO TABLA PUNTAJES

texto_principal = fuente.render("Top 10 mejores puntajes", True, COLOR_TEXTO)
alto_texto = texto_principal.get_height()
ancho_texto = texto_principal.get_width()
# debo tomar el ancho que uso para ubicar el principio de la tabla y centrarlo

texto_princiapl_x = (ANCHO_PANTALLA - ancho_texto) / 2
texto_princiapl_y = ALTO_PANTALLA * 0.05


# TABLA PUNTAJES
# Rectángulo que contiene toda la "tabla"

margen_inferior_tabla = ALTO_PANTALLA * 0.03
margen_superior_tabla = texto_princiapl_y + (ALTO_PANTALLA * 0.05)
espacio_por_fila = ALTO_PANTALLA * 0.06
cantidad_filas = 10


alto_cuadro = espacio_por_fila * cantidad_filas + \
    margen_inferior_tabla + margen_superior_tabla
ancho_cuadro = ANCHO_PANTALLA * 0.8

tabla_puntaje_x = ANCHO_PANTALLA * 0.1
tabla_puntaje_y = texto_princiapl_y + alto_texto + \
    ALTO_PANTALLA * 0.02  # margen extra visual
rect_tabla_puntaje = pygame.Rect(
    tabla_puntaje_x, tabla_puntaje_y, ancho_cuadro, alto_cuadro)


# BOTON VOLVER

# Debo primero medir el texto y en base a eso armar el cuadro


texto_boton = fuente.render("Volver", True, COLOR_TEXTO)
ancho_texto_boton = texto_boton.get_width()
alto_texto_boton = texto_boton.get_height()

boton_volver_ancho = ancho_texto_boton + ANCHO_PANTALLA * 0.04
boton_volver_alto = alto_texto_boton + ALTO_PANTALLA * 0.02

boton_volver_x = (ANCHO_PANTALLA - boton_volver_ancho) / 2

margen_inferior_pantalla = ALTO_PANTALLA * 0.05
boton_volver_y = ALTO_PANTALLA - boton_volver_alto - margen_inferior_pantalla

rect_boton_volver = pygame.Rect(
    boton_volver_x, boton_volver_y, boton_volver_ancho, boton_volver_alto)
texto_boton_centrado = texto_boton.get_rect(center=rect_boton_volver.center)


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

        pantalla.blit(texto_menu, (50, 50))

    if pantalla_puntajes == True:

        if bandera_musica_fondo == False:
            pygame.mixer.music.play(-1)
            bandera_musica_fondo = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.MOUSEBUTTONDOWN:

                if rect_boton_volver.collidepoint(evento.pos) == True:
                    if evento.button == 1:  # Boton izquierdo
                        pantalla_puntajes = False
                        pantalla_principal = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pantalla_puntajes = False
                    pantalla_principal = True

        pantalla.fill(COLOR_FONDO)
        pantalla.blit(texto_principal, (texto_princiapl_x, texto_princiapl_y))
        pygame.draw.rect(pantalla, (230, 230, 230),
                         rect_tabla_puntaje, border_radius=10)
        pygame.draw.rect(pantalla, (230, 230, 230),
                         rect_boton_volver, border_radius=10)
        pantalla.blit(texto_boton, texto_boton_centrado)

    pygame.display.flip()  # Actualiza TODA la pantalla del juego
