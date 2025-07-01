import pygame
from utils.constants import *

def dibujar_menu(ventana, fondo, opciones, fuente, ancho_ventana, opcion_seleccionada, color_normal, color_seleccionado, lista_rects):
    lista_rects.clear()

    espacio = 50  # Separacion entre opciones
    cantidad_opciones = len(opciones)
    altura_total = cantidad_opciones * espacio

    # Se baja el menu 120 pixeles por sobre el eje vertical
    y_inicial = (ventana.get_height() - altura_total) // 2 + 120

    indice = 0
    for texto in opciones:
        if indice == opcion_seleccionada:
            color = color_seleccionado
        else:
            color = color_normal

        render_texto = fuente.render(texto.upper(), True, color)
        rect_texto = render_texto.get_rect()
        rect_texto.centerx = ventana.get_width() // 2
        rect_texto.y = y_inicial + indice * espacio

        # Mostrar sombra solo si el texto es blanco , la variable se llama : (color_normal)
        if color == BLANCO:
            sombra = fuente.render(texto.upper(), True, (0, 0, 0))
            rect_sombra = sombra.get_rect()
            rect_sombra.centerx = rect_texto.centerx + 2
            rect_sombra.y = rect_texto.y + 2
            ventana.blit(sombra, rect_sombra)

        ventana.blit(render_texto, rect_texto)
        lista_rects.append(rect_texto)
        indice += 1



def obtener_opcion(rects_opciones, mouse_pos):
    '''
    Devuelve el índice de la opcion en el cual el rectangulo obtiene la posición del mouse.
    Si no hay colision, devuelve None.
    '''
    i = 0
    for rect in rects_opciones:
        if rect.collidepoint(mouse_pos):
            return i
        i += 1
    return None


def pantalla_opciones_resolucion(ventana, fuente, resoluciones, resolucion_actual):
    clock = pygame.time.Clock()
    seleccion = None
    volver = False
    ejecutando = True

    while ejecutando:
        ventana.fill((92, 148, 252))
        texto_titulo = fuente.render("RESOLUCIÓN", True, (255, 255, 255))
        ventana.blit(texto_titulo, (ventana.get_width()//2 - texto_titulo.get_width()//2, 50))

        y = 150
        botones = []
        for resolucion in resoluciones:
            texto = fuente.render(f"{resolucion[0]} x {resolucion[1]}", True, (0, 0, 0))
            rect = texto.get_rect(center=(ventana.get_width()//2, y))
            pygame.draw.rect(ventana, (255, 255, 255), rect.inflate(20, 10))
            ventana.blit(texto, rect)
            botones.append((rect, resolucion))
            y += 60

        # Botón Volver
        texto_volver = fuente.render("Volver", True, (0, 0, 0))
        rect_volver = texto_volver.get_rect(center=(ventana.get_width()//2, y + 40))
        pygame.draw.rect(ventana, (255, 0, 0), rect_volver.inflate(20, 10))
        ventana.blit(texto_volver, rect_volver)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for rect, resolucion in botones:
                    if rect.collidepoint(evento.pos):
                        seleccion = resolucion
                        ejecutando = False
                        break
                if rect_volver.collidepoint(evento.pos):
                    volver = True
                    ejecutando = False

        clock.tick(30)

    return seleccion, volver


