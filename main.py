import pygame
import sys
from utils.functions_score_menu  import *

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

pantalla_principal = True
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
