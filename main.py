import pygame
import sys
from utils.functions_score_menu import *
from utils.functions_game_menu import *
from utils.functions_main_menu import *
from utils.functions_game_logic import *
from utils.constants import *
from utils.functions_game_menu import *

RESOLUCIONES_DISPONIBLES = [
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1366, 768),
    (1600, 900),
    (1920, 1080)
]

# Inicializar pygame
pygame.init()
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Buscaminas - MARIO BROS")
icono = pygame.image.load("assets/images/icono.png")
pygame.display.set_icon(icono)

# Fondo y fuente
fondo = pygame.image.load("assets/images/fondofinal.png").convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
fuente = pygame.font.Font("assets/fonts/fuentemario.ttf", 20)

# Sonido
pygame.mixer.music.load("assets/sounds/sonido_fondo.mp3")
pygame.mixer.music.set_volume(0.2)
bandera_musica_fondo = False
musica_activada = True


# Menu
opciones = ["Iniciar Juego", "Puntajes", "Opciones", "Salir"]
rects_opciones = []

# Dificultad
botones_dif = hacer_boton(ventana, dic_botones_dif)
botones_dif_hover = crear_hover_botones(
    ventana, dic_botones_dif, img_dif_hover)


img_titulos = [
    {'titulo': 'assets/images/titulo_pantalla_dificultad.png',
        'superficie': ventana, 'rect': 'pantalla'},
    {'titulo': 'assets/images/titulo_boton_facil.png',
        'superficie': botones_dif[0]['rectangulo'], 'rect': 'boton'},
    {'titulo': 'assets/images/titulo_boton_medio.png',
        'superficie': botones_dif[1]['rectangulo'], 'rect': 'boton'},
    {'titulo': 'assets/images/titulo_boton_dificil.png',
        'superficie': botones_dif[2]['rectangulo'], 'rect': 'boton'}
]


# Timer
timer_segundos = 0
timer_minutos = 0

#elementos pantalla del juego
botones = hacer_boton(ventana, dic_botones)
hover_botones = crear_hover_botones(ventana, dic_botones, imagenes_hover)

timer = crear_timer(ventana, dic_timer)

buscaminas = crear_buscaminas(ventana, dic_buscaminas, timer[1].width + timer[1].x)

# Juego
pantalla_principal = True
pantalla_juego = False
pantalla_puntajes = False
pantalla_opciones = False
pantalla_dificultad = False
BUSCAMINAS_INICIADO = False
dificultad_elegida = None

primera_jugada = True
banderas_colocadas = 0

estado_derrota = False
celda_explotada = None

matriz_estado = None
matriz_juego = None

ruta_archivo_puntajes = "top_10.csv"


# Bucle principal
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    ancho_boton_musica = int(ANCHO * 0.15)
    alto_boton_musica = int(ALTO * 0.06)
    rec_boton_musica = pygame.Rect(
    ANCHO - ancho_boton_musica - 35, 10, ancho_boton_musica, alto_boton_musica)
    if pantalla_principal:
        mouse_pos = pygame.mouse.get_pos()
        opcion_seleccionada = obtener_opcion(rects_opciones, mouse_pos)
        # blit_centrado(ventana, fondo)
        ventana.blit(fondo, (0, 0))
        dibujar_menu(ventana, fondo, opciones, fuente, ANCHO,
                     opcion_seleccionada, BLANCO, NEGRO, rects_opciones)

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
                    pantalla_dificultad = True
                elif opcion_seleccionada == 1:
                    pantalla_principal = False
                    pantalla_puntajes = True
                elif opcion_seleccionada == 2:
                    pantalla_principal = False
                    pantalla_opciones = True
                elif opcion_seleccionada == 3:
                    pygame.quit()
                    sys.exit()

    # Boton de musica
        # Escalado de la fuente de texto del boton de musica proporcional a la pantalla
        tamaño_fuente_musica = max(12, int(ALTO * 0.03))
        fuente_musica = pygame.font.Font("assets/fonts/fuentemario.ttf", tamaño_fuente_musica)
        pygame.draw.rect(ventana, (0, 0, 0), rec_boton_musica, width=3)
        if musica_activada:
            texto_musica = "MUSICA ON"
        else:
            texto_musica = "MUSICA OFF"
        texto_render = fuente.render(texto_musica, True, BLANCO)
        texto_rect = texto_render.get_rect(center=rec_boton_musica.center)
        ventana.blit(texto_render, texto_rect)
        
    #Pantalla de Dificultad
    elif pantalla_dificultad:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:

                if botones_dif[0]['rectangulo'].collidepoint(evento.pos):
                    dificultad_elegida = 'facil'
                    (
                        matriz_estado, matriz_juego, columnas, minas, tamaño_celda,
                        imagen_mina, imagen_bandera, contador
                    ) = procesar_dificultad(
                        dificultad_elegida, dic_valores_dif, buscaminas[1].get_width(), CUBIERTA,
                        ventana, dic_contador
                    )
                    MINAS = minas
                    pantalla_dificultad = False
                    pantalla_juego = True

                elif botones_dif[1]['rectangulo'].collidepoint(evento.pos):
                    dificultad_elegida = 'normal'
                    (
                        matriz_estado, matriz_juego, columnas, minas, tamaño_celda,
                        imagen_mina, imagen_bandera, contador
                    ) = procesar_dificultad(
                        dificultad_elegida, dic_valores_dif, buscaminas[1].get_width(), CUBIERTA,
                        ventana, dic_contador
                    )
                    MINAS = minas
                    pantalla_dificultad = False
                    pantalla_juego = True

                elif botones_dif[2]['rectangulo'].collidepoint(evento.pos):
                    dificultad_elegida = 'dificil'

                    (
                        matriz_estado, matriz_juego, columnas, minas, tamaño_celda,
                        imagen_mina, imagen_bandera, contador
                    ) = procesar_dificultad(
                        dificultad_elegida, dic_valores_dif, buscaminas[1].get_width(), CUBIERTA,
                        ventana, dic_contador
                    )
                    MINAS = minas
                    pantalla_dificultad = False
                    pantalla_juego = True

        dibujar_pantalla_dif(ventana, img_titulos, ruta_fondo_dif)
        dibujar_botones(ventana, botones_dif, botones_dif_hover, mouse_pos)

    elif pantalla_juego:
        dic_elementos = [{'buscaminas': buscaminas, 'timer': timer,
                          'contador': contador, 'botones': botones, 'hover': hover_botones}]
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == timer[2] and BUSCAMINAS_INICIADO == True:
                timer_segundos += 1
                dic_timer[0]['texto'] = [timer_minutos, timer_segundos]
                timer = crear_timer(ventana, dic_timer)
                if timer_segundos >= 59:
                    timer_segundos = -1
                    timer_minutos += 1

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if estado_derrota:
                    if botones[0]['rectangulo'].collidepoint(evento.pos):
                        (
                            banderas_colocadas, contador, BUSCAMINAS_INICIADO,
                            timer_segundos, timer_minutos, dic_timer, timer, texto_timer,
                            matriz_estado, matriz_juego, primera_jugada, estado_derrota, celda_explotada
                        ) = reiniciar_juego(ventana, MINAS, fuente, dic_contador, dic_timer, columnas, columnas, COLOR_TIMER_NUMEROS, CUBIERTA)

                        pantalla_principal = True
                        pantalla_juego = False

                    elif botones[2]['rectangulo'].collidepoint(evento.pos):

                        (
                            banderas_colocadas, contador, BUSCAMINAS_INICIADO,
                            timer_segundos, timer_minutos, dic_timer, timer, texto_timer,
                            matriz_estado, matriz_juego, primera_jugada, estado_derrota, celda_explotada
                        ) = reiniciar_juego(
                            ventana, MINAS, fuente, dic_contador, dic_timer,
                            columnas, columnas, COLOR_TIMER_NUMEROS, CUBIERTA
                        )

                    continue

                if botones[0]['rectangulo'].collidepoint(evento.pos):

                    pantalla_principal = True
                    pantalla_juego = False
                    (
                        banderas_colocadas, contador, BUSCAMINAS_INICIADO,
                        timer_segundos, timer_minutos, dic_timer, timer, texto_timer,
                        matriz_estado, matriz_juego, primera_jugada, estado_derrota, celda_explotada
                    ) = reiniciar_juego(ventana, MINAS, fuente, dic_contador, dic_timer, columnas, columnas, COLOR_TIMER_NUMEROS, CUBIERTA)

                elif botones[1]['rectangulo'].collidepoint(evento.pos) and BUSCAMINAS_INICIADO:
                    BUSCAMINAS_INICIADO = False
                elif botones[2]['rectangulo'].collidepoint(evento.pos):

                    (
                        banderas_colocadas, contador, BUSCAMINAS_INICIADO,
                        timer_segundos, timer_minutos, dic_timer, timer, texto_timer,
                        matriz_estado, matriz_juego, primera_jugada, estado_derrota, celda_explotada
                    ) = reiniciar_juego(ventana, MINAS, fuente, dic_contador, dic_timer, columnas, columnas, COLOR_TIMER_NUMEROS, CUBIERTA)

                elif buscaminas[0].collidepoint(evento.pos):
                    if not estado_derrota:
                        BUSCAMINAS_INICIADO = True
                        x, y = evento.pos
                        columna = int(
                            (x - buscaminas[0].x) // tamaño_celda)
                        fila = int((y - buscaminas[0].y) // tamaño_celda)

                        if 0 <= fila < columnas and 0 <= columna < columnas:

                            if evento.button == 1:
                                if matriz_estado[fila][columna] != BANDERA:
                                    if primera_jugada:
                                        while True:
                                            matriz_juego = generar_matriz(
                                                columnas, columnas, MINAS, (fila, columna), MINA)
                                            if matriz_juego[fila][columna] == 0:
                                                break
                                        primera_jugada = False
                                        BUSCAMINAS_INICIADO = True

                                    exploto = descubrir(
                                        matriz_estado, matriz_juego, fila, columna, (MINA, DESCUBIERTA, BANDERA))
                                    if exploto:
                                        BUSCAMINAS_INICIADO = False
                                        estado_derrota = True
                                        celda_explotada = (fila, columna)
                                        for f in range(columnas):
                                            for c in range(columnas):
                                                if matriz_juego[f][c] == MINA:
                                                    matriz_estado[f][c] = DESCUBIERTA

                                        activar_sonido_derrota()
                                    else:
                                        total_celdas = columnas * columnas

                                        descubiertas = 0
                                        for fila in matriz_estado:
                                            for celda in fila:
                                                if celda == DESCUBIERTA:
                                                    descubiertas += 1

                                        if descubiertas == total_celdas - MINAS:
                                            BUSCAMINAS_INICIADO = False
                                            config_victoria = obtener_config_cuadro_victoria(
                                                ventana, ANCHO, ALTO)
                                            tiempo_empleado = timer_minutos * 60 + timer_segundos
                                            penalidad = definir_penalidad(
                                                dificultad_elegida)
                                            puntaje_final = calcular_puntaje(
                                                penalidad, tiempo_empleado)
                                            nombre_usuario = mostrar_pantalla_victoria(
                                                ventana, puntaje_final, config_victoria)
                                            datos = leer_puntajes(
                                                config_victoria["ruta_archivo"])
                                            datos_finales = validar_datos_archivo(
                                                datos, nombre_usuario, puntaje_final)
                                            crear_sobreescribir_archivo(
                                                datos_finales, config_victoria["ruta_archivo"])
                                            (
                                                banderas_colocadas, contador, BUSCAMINAS_INICIADO,
                                                timer_segundos, timer_minutos, dic_timer, timer, texto_timer,
                                                matriz_estado, matriz_juego, primera_jugada, estado_derrota, celda_explotada
                                            ) = reiniciar_juego(
                                                ventana, MINAS, fuente, dic_contador, dic_timer,
                                                columnas, columnas, COLOR_TIMER_NUMEROS, CUBIERTA
                                            )
                                            pantalla_juego = False
                                            pantalla_principal = True

                            elif evento.button == 3:
                                if matriz_estado[fila][columna] == CUBIERTA:
                                    if banderas_colocadas < MINAS:
                                        matriz_estado[fila][columna] = BANDERA
                                        banderas_colocadas += 1
                                        contador = crear_contador(
                                        ventana, dic_contador, MINAS - banderas_colocadas)
                                    else :
                                        #Se puede poner sonido de limite alcanzado
                                        pass
                                elif matriz_estado[fila][columna] == BANDERA:
                                     matriz_estado[fila][columna] = CUBIERTA
                                     banderas_colocadas -= 1
                                     contador = crear_contador(
                                        ventana, dic_contador, MINAS - banderas_colocadas)

        ventana.blit(fondo_pantall_juego, (0, 0))

        dibujar_elementos_pantalla(
            ventana, dic_elementos, COLOR_RECTANGULOS, mouse_pos)

        if matriz_juego:
            for fila in range(columnas):
                for columna in range(columnas):

                    x = buscaminas[0].x + columna * tamaño_celda
                    y = buscaminas[0].y + fila * tamaño_celda
                    estado = matriz_estado[fila][columna]

                    if estado == CUBIERTA:
                        pygame.draw.rect(
                            ventana, COLOR_CELDA_OCULTA, (x, y, tamaño_celda, tamaño_celda))
                    elif estado == BANDERA:

                        pygame.draw.rect(
                            ventana, COLOR_DESCUBIERTA, (x, y, tamaño_celda, tamaño_celda))
                        imagen_rect = imagen_bandera.get_rect()
                        imagen_rect.center = (
                            x + tamaño_celda // 2, y + tamaño_celda // 2)
                        ventana.blit(imagen_bandera, imagen_rect)

                    elif estado == DESCUBIERTA:

                        if celda_explotada == (fila, columna):

                            pygame.draw.rect(
                                ventana, (255, 0, 0), (x, y, tamaño_celda, tamaño_celda))
                        else:
                            pygame.draw.rect(
                                ventana, COLOR_DESCUBIERTA, (x, y, tamaño_celda, tamaño_celda))
                        valor = matriz_juego[fila][columna]

                        if valor == MINA:
                            imagen_rect = imagen_mina.get_rect()
                            imagen_rect.center = (
                                x + tamaño_celda // 2, y + tamaño_celda // 2)
                            ventana.blit(imagen_mina, imagen_rect)

                        if valor > 0:
                            color = colores_numeros.get(valor, (0, 0, 0))
                            texto = fuente.render(str(valor), True, color)
                            rect = texto.get_rect(
                                center=(x + tamaño_celda / 2, y + tamaño_celda / 2))
                            ventana.blit(texto, rect)

                    pygame.draw.rect(ventana, COLOR_CELDA_MARCO,
                                     (x, y, tamaño_celda, tamaño_celda), width=2)

    elif pantalla_puntajes == True:

        config_puntajes = obtener_config_puntajes(ventana, ANCHO, ALTO)
        volver_al_menu, bandera_musica_fondo = ejecutar_pantalla_puntajes(
    ventana, config_puntajes, bandera_musica_fondo, musica_activada
)

        if volver_al_menu:
            pantalla_puntajes = False
            pantalla_principal = True
    
    
    
    # Pantalla de Opciones
    elif pantalla_opciones:
        nueva_resolucion, volver = pantalla_opciones_resolucion(
            ventana, fuente, RESOLUCIONES_DISPONIBLES, (ANCHO, ALTO)
        )

        if nueva_resolucion:
            ANCHO, ALTO = nueva_resolucion
            ventana = pygame.display.set_mode((ANCHO, ALTO))
            fondo = pygame.transform.scale(
                pygame.image.load("assets/images/fondofinal.png"), (ANCHO, ALTO))
            fondo_pantall_juego = pygame.transform.scale(
                pygame.image.load('assets/images/fondo_pantalla_juego.jpg'), (ANCHO, ALTO))
            pantalla_dificultad = pygame.transform.scale(
                pygame.image.load('assets/images/fondo_pantalla_dificultad.jpg'), (ANCHO, ALTO))
            botones = hacer_boton(ventana, dic_botones)
            hover_botones = crear_hover_botones(ventana, dic_botones, imagenes_hover)
            botones_dif = hacer_boton(ventana, dic_botones_dif)
            botones_dif_hover = crear_hover_botones(ventana, dic_botones_dif, img_dif_hover)
            timer = crear_timer(ventana, dic_timer)
            buscaminas = crear_buscaminas(ventana, dic_buscaminas, timer[1].width + timer[1].x)
            contador = crear_contador(ventana, dic_contador, 0)
            img_titulos = [
                {'titulo': 'assets/images/titulo_pantalla_dificultad.png',
                    'superficie': ventana, 'rect': 'pantalla'},
                {'titulo': 'assets/images/titulo_boton_facil.png',
                    'superficie': botones_dif[0]['rectangulo'], 'rect': 'boton'},
                {'titulo': 'assets/images/titulo_boton_medio.png',
                    'superficie': botones_dif[1]['rectangulo'], 'rect': 'boton'},
                {'titulo': 'assets/images/titulo_boton_dificil.png',
                    'superficie': botones_dif[2]['rectangulo'], 'rect': 'boton'}
]

        if nueva_resolucion or volver:
            pantalla_opciones = False
            pantalla_principal = True
            pantalla_dificultad = False
    
    
    pygame.display.flip()

pygame.quit()
sys.exit()
