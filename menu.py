import pygame
import sys

# Inicializar pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú Principal")

# Colores
NEGRO = (0, 0, 0)
AZUL = (0, 120, 255)
BLANCO = (255,255,255)

# Cargar imagen de fondo
fondo = pygame.image.load("UTN-Pygame/assets/images/fondofinal.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))  # Ajusta al tamaño de la ventana

# Fuente
fuente = pygame.font.Font("UTN-Pygame/assets/fonts/fuentemario.ttf", 20)

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

# Bucle principal
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    opcion_seleccionada = obtener_opcion(mouse_pos)
    dibujar_menu(opcion_seleccionada)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if opcion_seleccionada == 0:
                print("Iniciar Juego seleccionado")
            elif opcion_seleccionada == 1:
                print("Puntajes seleccionado")
            elif opcion_seleccionada == 2:
                print("Opciones seleccionado")
            elif opcion_seleccionada == 3:
                print("Salir seleccionado")
                pygame.quit()
                sys.exit()

# Cerrar pygame
pygame.quit()
sys.exit()