

# import pygame
# from functions_game_menu import *

# pygame.init()

# ANCHO_PANTALLA = 1280
# ALTO_PANTALLA = 600
# pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
# pygame.display.set_caption('Busca Minas')


# #diccionarios de los elementos

# dic_buscaminas = [{'dimension':0.95, 'x':0.55, 'y':0.05}]

# dic_botones = [
#     {'ancho': 0.19, 'alto': 0.14, 'x': 0.06 , 'y': 0.80 ,'texto': 'assets/images/texto_volver.png', 'fondo': 'assets/images/fondo_boton.png'},   
#     {'ancho': 0.19, 'alto': 0.14, 'x': 0.06 , 'y': 0.62 ,'texto': 'assets/images/texto_pausar.png', 'fondo': 'assets/images/fondo_boton.png'},
#     {'ancho': 0.12, 'alto': 0.16, 'x': 0.09 , 'y': 0.44 ,'texto': 'assets/images/honguito_verde.png','fondo': 'assets/images/fondo_boton.png'}
#     ]

# dic_contador = [{'ancho': 0.14, 'alto': 0.14, 'x': 0.082 , 'y': 0.25, 'fuente':0.65}]

# dic_timer = [
#     {'ancho': 0.22, 'alto': 0.15, 'x': 0.04 , 'y': 0.05 ,'texto': [0,0] ,'color': (255, 0, 0), 'fuente':80}
#      ]


# #variables
# fondo_pantall_juego = pygame.image.load('assets/images/fondo_pantalla_juego.jpg')
# fondo_pantall_juego = pygame.transform.scale(fondo_pantall_juego, (ANCHO_PANTALLA, ALTO_PANTALLA))

# COLOR_RECTANGULOS = (0, 0, 0)

# #borrar
# '============'
# FILAS = 8
# COLUMNAS = 8

# COLOR_CELDA_OCULTA = (134, 47, 16)
# COLOR_CELDA_MARCO = (64, 21, 5)
# '============'

# minas = 0

# timer_segundos = 0
# timer_minutos = 0

# #elementos del juego

# buscaminas = crear_buscaminas(pantalla, dic_buscaminas)

# botones = hacer_boton(pantalla,dic_botones)    
# hover_botones = crear_hover_botones(pantalla, dic_botones)

# contador = crear_contador(pantalla, dic_contador, minas)

# timer = crear_timer(pantalla,dic_timer)


# #Banderas

# BUSCAMINAS_INICIADO = False
# pantalla_juego = True

# #BUCLE JUEGO
# while True:

#     if pantalla_juego == True:
#         mouse_pos = pygame.mouse.get_pos()
#         dic_elementos = [{'buscaminas':buscaminas, 'timer':timer, 'contador':contador, 'botones':botones, 'hover':hover_botones}]

#         for evento in pygame.event.get():
#             if evento.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()

#             if evento.type == timer[2] and BUSCAMINAS_INICIADO == True:
#                 timer_segundos += 1
#                 dic_timer[0]['texto'] = [timer_minutos,timer_segundos]
#                 timer = crear_timer(pantalla,dic_timer)
#                 if timer_segundos >= 59:
#                     timer_segundos = -1
#                     timer_minutos += 1


#             if evento.type == pygame.MOUSEBUTTONDOWN: 

#                     if botones[0]['rectangulo'].collidepoint(evento.pos) == True:
#                         print("Clickeaste sobre el volver.") #BORRAR
                    
#                     if botones[1]['rectangulo'].collidepoint(evento.pos) == True and BUSCAMINAS_INICIADO == True:
#                         print("Clickeaste sobre el pausar.") #BORRAR
#                         BUSCAMINAS_INICIADO = False

#                     if botones[2]['rectangulo'].collidepoint(evento.pos) == True:
#                         print("Clickeaste sobre el reiniciar.") #BORRAR
#                         BUSCAMINAS_INICIADO = False
#                         timer_segundos = 0
#                         timer_minutos = 0
#                         dic_timer[0]['texto'] = [timer_minutos,timer_segundos]
#                         timer = crear_timer(pantalla,dic_timer)

#                     if buscaminas[0].collidepoint(evento.pos) == True:
#                         print("Clickeaste sobre el cuadro de buscaminas.") #BORRAR
#                         BUSCAMINAS_INICIADO = True


#         pantalla.blit(fondo_pantall_juego, (0,0))
#         dibujar_elementos_pantalla(pantalla, dic_elementos, COLOR_RECTANGULOS, mouse_pos)

#         for fila in range(FILAS): #esto es solo visual para que se vea como quedaria las celdas del buscaminas si queres no lo pongas
#             for columna in range(COLUMNAS):
#                 tamaño_celda =  int(buscaminas[2] // COLUMNAS)
#                 posicion_x_celda = buscaminas[0].x + columna * tamaño_celda
#                 posicion_y_celda = buscaminas[0].y + fila * tamaño_celda
        
#                 pygame.draw.rect(pantalla,COLOR_CELDA_OCULTA,(posicion_x_celda, posicion_y_celda, tamaño_celda, tamaño_celda))
#                 pygame.draw.rect(pantalla,COLOR_CELDA_MARCO,(posicion_x_celda, posicion_y_celda, tamaño_celda, tamaño_celda), width=2)


#     pygame.display.flip()


# CODIGO COMENTADO PARA DEJAR CONSTANCIA DE QUE SE COPIÓ LOS ARCHIVOS Y SE PUSO EN EL MAIN CORRESPONDIENTE