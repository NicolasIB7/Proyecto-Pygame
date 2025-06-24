import pygame
import sys
from utils.functions_score_menu import *


# Inicializar pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Buscaminas - MARIO BROS")
icono = pygame.image.load("assets/images/icono.png")
pygame.display.set_icon(icono)


# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 120, 255)
BLANCO = (255, 255, 255)


# Cargar imagen de fondo
fondo = pygame.image.load("assets/images/fondofinal.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Fuente

fuente = pygame.font.Font("assets/fonts/fuentemario.ttf", 20)

# Sonido
ruta_sonido = "assets/sounds/sonido_fondo.mp3"
pygame.mixer.music.load(ruta_sonido)
pygame.mixer.music.set_volume(0.5)
bandera_musica_fondo = False


# Opciones del menú
opciones = ["Iniciar Juego", "Puntajes", "Opciones", "Salir"]
rects_opciones = []


def dibujar_menu(opcion_seleccionada):
    ventana.blit(fondo, (0, 0))  # Dibuja el fondo
    rects_opciones.clear()  # Limpiamos los anteriores
    for i, texto in enumerate(opciones):
        color = NEGRO if i == opcion_seleccionada else BLANCO
        render_texto = fuente.render(texto, True, color)
        rect = render_texto.get_rect(center=(ANCHO // 2, 330 + i * 60))
        ventana.blit(render_texto, rect)
        rects_opciones.append(rect)
    pygame.display.flip()


def obtener_opcion(mouse_pos):
    for i, rect in enumerate(rects_opciones):
        if rect.collidepoint(mouse_pos):
            return i
    return None


# Configuracion para menu puntajes
config_puntajes = obtener_config_puntajes(pygame, ventana, ANCHO, ALTO)


# # VARIABLES DE PANTALLA PRINCIPAL




COLOR_TEXTO_BOTONES = (255, 255, 255)


# CUADRO BUSCAMINAS
ancho_buscaminas = ANCHO * 0.65
alto_buscaminas = ALTO * 0.85
posicion_x_buscaminas = ANCHO * 0.3
posicion_y_buscaminas = ALTO * 0.08

rec_buscaminas = pygame.Rect(
    posicion_x_buscaminas, posicion_y_buscaminas, ancho_buscaminas, alto_buscaminas)


# borrar
'============'
FILAS = 8
COLUMNAS = 8
'============'

tamaño_celda = int(ancho_buscaminas / COLUMNAS)
COLOR_CELDA_OCULTA = (134, 47, 16)
COLOR_CELDA_MARCO = (64, 21, 5)


# BOTONES

tamaño_fuente_botones = int(((35*ANCHO)/800 + (35*ALTO)/600)/2)
ancho_boton = ANCHO * 0.19
alto_boton = ALTO * 0.14
posicion_x_boton = ANCHO * 0.06
posicion_y_boton = ALTO * 0.75
fuente = pygame.font.SysFont('freesansbold', tamaño_fuente_botones)


# boton volver
rec_boton_volver = pygame.Rect(
    posicion_x_boton, posicion_y_boton, ancho_boton, alto_boton)
texto_volver = fuente.render("VOLVER", True, COLOR_TEXTO_BOTONES)
texto_boton_volver = texto_volver.get_rect(center=rec_boton_volver.center)

# boton reiniciar
rec_boton_reiniciar = pygame.Rect(
    posicion_x_boton, posicion_y_boton-200, ancho_boton, alto_boton)
texto_reiniciar = fuente.render("REINICIAR", True, COLOR_TEXTO_BOTONES)
text_boton_reiniciar = texto_reiniciar.get_rect(
    center=rec_boton_reiniciar.center)

# boton pausar
rec_boton_pausar = pygame.Rect(
    posicion_x_boton, posicion_y_boton-100, ancho_boton, alto_boton)
texto_pausar = fuente.render("PAUSAR", True, COLOR_TEXTO_BOTONES)
texto_boton_pausar = texto_pausar.get_rect(center=rec_boton_pausar.center)


# TIMER

def hacer_cadena_timer(segundos: int, minutos: int) -> str:
    """
    docu
    """
    timer_segundos = f'{segundos}'
    timer_minutos = f'{minutos}'

    if segundos < 10:
        timer_segundos = '0' + f'{segundos}'

    if minutos < 10:
        timer_minutos = '0' + f'{minutos}'

    cadena = f'{timer_minutos}:{timer_segundos}'

    return cadena


ancho_cuadro_timer = ANCHO * 0.25
alto_cuadro_timer = ALTO * 0.15
posicion_x_timer = ANCHO * 0.03
posicion_y_timer = ALTO * 0.05
COLOR_TIMER_NUMEROS = (255, 0, 0)
COLOR_FONDO = (34, 139, 27)
COLOR_RECTANGULOS = (0, 0, 0)

cuadro_timer = pygame.Rect(
    posicion_x_timer, posicion_y_timer, ancho_cuadro_timer, alto_cuadro_timer)

tamaño_fuente_timer = int(((80*ANCHO)/800 + (80*ALTO)/600)/2)

evento_segundo = pygame.USEREVENT + 1
pygame.time.set_timer(evento_segundo, 1000)
# fuente = pygame.font.SysFont('freesansbold', tamaño_fuente_timer)
timer_segundos = 0
timer_minutos = 0
texto_timer = fuente.render("00:00", True, COLOR_TIMER_NUMEROS)
text_rect = texto_timer.get_rect(center=cuadro_timer.center)


# ##########################
BUSCAMINAS_INICIADO = False

pantalla_principal = True
pantalla_juego = False
pantalla_puntajes = False



# Bucle principal
running = True
while running:

    if pantalla_principal == True:
        mouse_pos = pygame.mouse.get_pos()
        opcion_seleccionada = obtener_opcion(mouse_pos)
        dibujar_menu(opcion_seleccionada)

        # sonido
        if bandera_musica_fondo == False:
            pygame.mixer.music.play(-1)
            bandera_musica_fondo = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if opcion_seleccionada == 0:
                    print("Iniciar Juego seleccionado")
                    pantalla_principal = False
                    pantalla_juego = True
                elif opcion_seleccionada == 1:
                    print("Puntajes seleccionado")
                    pantalla_principal = False
                    pantalla_puntajes = True
                elif opcion_seleccionada == 2:
                    print("Opciones seleccionado")
                elif opcion_seleccionada == 3:
                    print("Salir seleccionado")
                    pygame.quit()
                    sys.exit()

    if pantalla_juego == True:
        

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == evento_segundo and BUSCAMINAS_INICIADO == True:
                timer_segundos += 1
                texto_timer = fuente.render(hacer_cadena_timer(
                    timer_segundos, timer_minutos), True, COLOR_TIMER_NUMEROS)

                if timer_segundos == 59:
                    timer_segundos = -1
                    timer_minutos += 1

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if rec_boton_volver.collidepoint(evento.pos) == True:
                    print("Clickeaste sobre el volver.")  # BORRAR
                    pantalla_principal = True
                    pantalla_juego = False

                if rec_boton_pausar.collidepoint(evento.pos) == True:
                    print("Clickeaste sobre el pausar.")  # BORRAR
                    BUSCAMINAS_INICIADO = not BUSCAMINAS_INICIADO

                if rec_boton_reiniciar.collidepoint(evento.pos) == True:
                    print("Clickeaste sobre el reiniciar.")  # BORRAR
                    BUSCAMINAS_INICIADO = False
                    timer_segundos = 0
                    timer_minutos = 0
                    texto_timer = fuente.render(
                        "00:00", True, COLOR_TIMER_NUMEROS)

                if rec_buscaminas.collidepoint(evento.pos) == True:
                    print("Clickeaste sobre el cuadro de buscaminas.")  # BORRAR
                    BUSCAMINAS_INICIADO = True

        ventana.fill(COLOR_FONDO)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS, rec_buscaminas, width=5)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS, rec_boton_volver, width=5)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS,
                         rec_boton_reiniciar, width=5)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS, rec_boton_pausar, width=5)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS,
                         cuadro_timer, border_radius=15)
        ventana.blit(texto_timer, text_rect)
        ventana.blit(texto_volver, texto_boton_volver)
        ventana.blit(texto_reiniciar, text_boton_reiniciar)
        ventana.blit(texto_pausar, texto_boton_pausar)

        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                posicion_x_celda = posicion_x_buscaminas + columna * tamaño_celda
                posicion_y_celda = posicion_y_buscaminas + fila * tamaño_celda

                pygame.draw.rect(ventana, COLOR_CELDA_OCULTA, (posicion_x_celda,
                                 posicion_y_celda, tamaño_celda, tamaño_celda))
                pygame.draw.rect(ventana, COLOR_CELDA_MARCO, (posicion_x_celda,
                                 posicion_y_celda, tamaño_celda, tamaño_celda), width=2)

    if pantalla_puntajes == True:
        ventana.fill((107, 140, 255))
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
    pygame.display.flip()

# Cerrar pygame
pygame.quit()
sys.exit()
