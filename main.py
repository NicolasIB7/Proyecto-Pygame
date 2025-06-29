import pygame
import sys
from utils.functions_score_menu import *
from utils.functions_game_menu import hacer_cadena_timer
from utils.functions_main_menu import dibujar_menu, obtener_opcion
from utils.functions_game_logic import (
    generar_matriz, descubrir,
    CUBIERTA, DESCUBIERTA, BANDERA, MINA
)
from utils.constantes import *
from utils.functions_victory_logic import *

# Inicializar pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Buscaminas - MARIO BROS")
icono = pygame.image.load("assets/images/icono.png")
pygame.display.set_icon(icono)

# Fondo y fuente
fondo = pygame.image.load("assets/images/fondofinal.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
fuente = pygame.font.Font("assets/fonts/fuentemario.ttf", 20)

# Sonido
pygame.mixer.music.load("assets/sounds/sonido_fondo.mp3")
pygame.mixer.music.set_volume(0.5)
bandera_musica_fondo = False
musica_activada = True

# Botón silenciar música
ancho_boton_musica = ANCHO * 0.15
alto_boton_musica = ALTO * 0.06
rec_boton_musica = pygame.Rect(ANCHO - ancho_boton_musica - 10, 10, ancho_boton_musica, alto_boton_musica)

# Menu
opciones = ["Iniciar Juego", "Puntajes", "Opciones", "Salir"]
rects_opciones = []

# Puntajes
config_puntajes = obtener_config_puntajes(ventana, ANCHO, ALTO)

# Timer
evento_segundo = pygame.USEREVENT + 1
pygame.time.set_timer(evento_segundo, 1000)
timer_segundos = 0
timer_minutos = 0
texto_timer = fuente.render("00:00", True, COLOR_TIMER_NUMEROS)
text_rect = texto_timer.get_rect(center=cuadro_timer.center)

# Juego
pantalla_principal = True
pantalla_juego = False
pantalla_puntajes = False
pantalla_prueba = False
BUSCAMINAS_INICIADO = False

FILAS = 8
COLUMNAS = 8
MINAS = 10
primera_jugada = True
# matriz_estado = [[CUBIERTA for _ in range(COLUMNAS)] for _ in range(FILAS)]
# matriz_juego = None
# matriz_juego = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]

matriz_estado = []
for fila in range(FILAS):
    fila_estado = []
    for columna in range(COLUMNAS):
        fila_estado.append(CUBIERTA)
    matriz_estado.append(fila_estado)

matriz_juego = None 

matriz_juego = []
for fila in range(FILAS):
    fila_juego = []
    for columna in range(COLUMNAS):
        fila_juego.append(0)
    matriz_juego.append(fila_juego)

estado_derrota = False
celda_explotada = None

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

imagen_mina = pygame.transform.scale(
    pygame.image.load("assets/images/imagen_mina.png"),
    (tamaño_celda, tamaño_celda)
)
imagen_bandera = pygame.transform.scale(pygame.image.load("assets/images/imagen_bandera.png"), (tamaño_celda, tamaño_celda))



# Bucle principal
running = True
while running:
    if pantalla_principal:
        mouse_pos = pygame.mouse.get_pos()
        opcion_seleccionada = obtener_opcion(rects_opciones, mouse_pos)
        dibujar_menu(ventana, fondo, opciones, fuente, ANCHO, opcion_seleccionada, NEGRO, BLANCO, rects_opciones)

        if not bandera_musica_fondo:
            pygame.mixer.music.play(-1)
            bandera_musica_fondo = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rec_boton_musica.collidepoint(evento.pos):
                    musica_activada = not musica_activada
                    if musica_activada:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                elif opcion_seleccionada == 0:
                    pantalla_principal = False
                    pantalla_juego = True
                elif opcion_seleccionada == 1:
                    pantalla_principal = False
                    pantalla_puntajes = True
                elif opcion_seleccionada == 3:
                    pygame.quit()
                    sys.exit()

        pygame.draw.rect(ventana, (0, 0, 0), rec_boton_musica, width=3)
        texto_musica = "MUSICA ON" if musica_activada else "MUSICA OFF"
        ventana.blit(fuente.render(texto_musica, True, BLANCO), rec_boton_musica)

    elif pantalla_juego:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == evento_segundo and BUSCAMINAS_INICIADO:
                timer_segundos += 1
                if timer_segundos == 60:
                    timer_segundos = 0
                    timer_minutos += 1
                texto_timer = fuente.render(hacer_cadena_timer(timer_segundos, timer_minutos), True, COLOR_TIMER_NUMEROS)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                
                
                
                
                # CONTROLA SI ESTAMOS ANTE UNA DERROTA:
                if estado_derrota:
                    if rec_boton_volver.collidepoint(evento.pos):
                        pantalla_principal = True
                        pantalla_juego = False
                        estado_derrota = False
                        celda_explotada = None
                    elif rec_boton_reiniciar.collidepoint(evento.pos):
                        BUSCAMINAS_INICIADO = False
                        timer_segundos = 0
                        timer_minutos = 0
                        texto_timer = fuente.render("00:00", True, COLOR_TIMER_NUMEROS)
                        # matriz_estado = [[CUBIERTA for _ in range(COLUMNAS)] for _ in range(FILAS)]
                        # matriz_juego = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]
                        matriz_estado = []
                        for fila in range(FILAS):
                            fila_estado = []
                            for columna in range(COLUMNAS):
                                fila_estado.append(CUBIERTA)
                            matriz_estado.append(fila_estado)

                        matriz_juego = []
                        for fila in range(FILAS):
                            fila_juego = []
                            for columna in range(COLUMNAS):
                                fila_juego.append(0)
                            matriz_juego.append(fila_juego)
                        
                        primera_jugada = True
                        estado_derrota = False
                        celda_explotada = None

                        
                # SI NO ESTAMOS ANTES UNA DERROTA APLICO LO QUE YA ESTABA        
                else:        
                    if rec_boton_volver.collidepoint(evento.pos):
                        pantalla_principal = True
                        pantalla_juego = False
                    elif rec_boton_pausar.collidepoint(evento.pos):
                        BUSCAMINAS_INICIADO = not BUSCAMINAS_INICIADO
                    elif rec_boton_reiniciar.collidepoint(evento.pos):
                        BUSCAMINAS_INICIADO = False
                        timer_segundos = 0
                        timer_minutos = 0
                        texto_timer = fuente.render("00:00", True, COLOR_TIMER_NUMEROS)
                        # matriz_estado = [[CUBIERTA for _ in range(COLUMNAS)] for _ in range(FILAS)]
                        # matriz_juego = [[0 for _ in range(COLUMNAS)] for _ in range(FILAS)]  
                        
                        matriz_estado = []
                        for fila in range(FILAS):
                            fila_estado = []
                            for columna in range(COLUMNAS):
                                fila_estado.append(CUBIERTA)
                            matriz_estado.append(fila_estado)

                        matriz_juego = []
                        for fila in range(FILAS):
                            fila_juego = []
                            for columna in range(COLUMNAS):
                                fila_juego.append(0)
                            matriz_juego.append(fila_juego)

                        primera_jugada = True
                    elif rec_buscaminas.collidepoint(evento.pos):
                        x, y = evento.pos
                        columna = int((x - posicion_x_buscaminas) // tamaño_celda)
                        fila = int((y - posicion_y_buscaminas) // tamaño_celda)

                        if 0 <= fila < FILAS and 0 <= columna < COLUMNAS:
                            if evento.button == 1:
                                if matriz_estado[fila][columna] != BANDERA:
                                    if primera_jugada:
                                        matriz_juego = generar_matriz(FILAS, COLUMNAS, MINAS, (fila, columna))
                                        primera_jugada = False
                                        BUSCAMINAS_INICIADO = True
                                    exploto  = descubrir(matriz_estado, matriz_juego, fila, columna)
                                    
                                    
                                    
                                    # SI DESCUBRIMOS UNA MINA ENTONCES COMENZARÁ EL EVENTO DE DERROTA.(PUNTO 5)
                                    if exploto:
                                        BUSCAMINAS_INICIADO = False
                                        estado_derrota = True
                                        celda_explotada = (fila, columna)
                                        for f in range(FILAS):
                                            for c in range(COLUMNAS):
                                                if matriz_juego[f][c] == MINA:
                                                    matriz_estado[f][c] = DESCUBIERTA
                                        # sonido derrota
                                        pygame.mixer.music.stop()
                                        sonido_derrota = pygame.mixer.Sound("assets/sounds/sonido_derrota.mp3")
                                        sonido_derrota.play()
                                        
                                        
                                        
                                    # SINO VERIFICA LA VICTORIA Y EJECUTA EL COMPONENTE DE VICTORIA.  
                                    else:
                                        total_celdas = FILAS * COLUMNAS
                                        descubiertas = 0
                                        for fila in matriz_estado:
                                            for celda in fila:
                                                if celda == DESCUBIERTA:
                                                    descubiertas += 1

                                        if descubiertas == total_celdas - MINAS:
                                            BUSCAMINAS_INICIADO = False
                                            config_victoria = obtener_config_cuadro_victoria(ventana, ANCHO, ALTO)

                                            # tiempo_empleado = 100
                                            tiempo_empleado = tiempo_empleado = timer_minutos * 60 + timer_segundos
                                            penalidad = definir_penalidad("Medio")
                                            puntaje_final = calcular_puntaje(penalidad, tiempo_empleado)
                                            nombre_usuario = mostrar_pantalla_victoria(ventana, puntaje_final, config_victoria)

                                            datos = leer_puntajes("top_10.csv")
                                            datos_finales = validar_datos_archivo(datos, nombre_usuario, puntaje_final)
                                            crear_sobreescribir_archivo(datos_finales, "top_10.csv")
                                            pantalla_juego = False
                                            pantalla_principal = True
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                            elif evento.button == 3:
                                if matriz_estado[fila][columna] == CUBIERTA:
                                    matriz_estado[fila][columna] = BANDERA
                                elif matriz_estado[fila][columna] == BANDERA:
                                    matriz_estado[fila][columna] = CUBIERTA

        ventana.fill(COLOR_FONDO)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS, rec_buscaminas, width=5)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS, rec_boton_volver, width=5)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS, rec_boton_reiniciar, width=5)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS, rec_boton_pausar, width=5)
        pygame.draw.rect(ventana, COLOR_RECTANGULOS, cuadro_timer, border_radius=15)
        ventana.blit(texto_timer, text_rect)
        ventana.blit(fuente.render("VOLVER", True, COLOR_TEXTO_BOTONES), rec_boton_volver)
        ventana.blit(fuente.render("REINICIAR", True, COLOR_TEXTO_BOTONES), rec_boton_reiniciar)
        ventana.blit(fuente.render("PAUSAR", True, COLOR_TEXTO_BOTONES), rec_boton_pausar)

        if matriz_juego:
            for fila in range(FILAS):
                for columna in range(COLUMNAS):
                    x = posicion_x_buscaminas + columna * tamaño_celda
                    y = posicion_y_buscaminas + fila * tamaño_celda
                    estado = matriz_estado[fila][columna]

                    if estado == CUBIERTA:
                        pygame.draw.rect(ventana, COLOR_CELDA_OCULTA, (x, y, tamaño_celda, tamaño_celda))
                    elif estado == BANDERA:
                        # pygame.draw.rect(ventana, (255, 0, 0), (x, y, tamaño_celda, tamaño_celda))

                        pygame.draw.rect(ventana, COLOR_DESCUBIERTA, (x, y, tamaño_celda, tamaño_celda))
                        ventana.blit(imagen_bandera, (x, y))

                    elif estado == DESCUBIERTA:
                        
                        if celda_explotada == (fila, columna):

                            pygame.draw.rect(ventana, (255, 0, 0), (x, y, tamaño_celda, tamaño_celda))
                        else:
                            pygame.draw.rect(ventana, COLOR_DESCUBIERTA, (x, y, tamaño_celda, tamaño_celda))
                        valor = matriz_juego[fila][columna]
                        
                        #DIBUJO MINA EN EL VALOR
                        if valor == MINA:
                            ventana.blit(imagen_mina, (x, y))
                        if valor > 0:
                            color = colores_numeros.get(valor, (0, 0, 0))
                            texto = fuente.render(str(valor), True, color)
                            rect = texto.get_rect(center=(x + tamaño_celda / 2, y + tamaño_celda / 2))
                            ventana.blit(texto, rect)

                    pygame.draw.rect(ventana, COLOR_CELDA_MARCO, (x, y, tamaño_celda, tamaño_celda), width=2)

    elif pantalla_puntajes == True:

        volver_al_menu, bandera_musica_fondo = ejecutar_pantalla_puntajes(ventana, config_puntajes, bandera_musica_fondo)
        if volver_al_menu:
            pantalla_puntajes = False
            bandera_musica_fondo = False
            desactivar_sonido()
            pantalla_principal = True



    pygame.display.flip()

pygame.quit()
sys.exit()