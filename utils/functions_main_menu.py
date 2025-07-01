import pygame

def dibujar_menu(ventana, fondo, opciones, fuente, ANCHO, opcion_seleccionada, NEGRO, BLANCO, rects_opciones):
    '''
    Documentación
    '''
    ventana.blit(fondo, (0, 0))  
    rects_opciones.clear()

    for i, texto in enumerate(opciones):
        color = NEGRO if i == opcion_seleccionada else BLANCO
        render_texto = fuente.render(texto, True, color)
        rect = render_texto.get_rect(center=(ANCHO // 2, 330 + i * 60))
        ventana.blit(render_texto, rect)
        rects_opciones.append(rect)

def obtener_opcion(rects_opciones, mouse_pos):
    '''
    Documentación
    '''

    for i, rect in enumerate(rects_opciones):
        if rect.collidepoint(mouse_pos):
            return i
    return None



