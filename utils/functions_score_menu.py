import pygame


def obtener_config_puntajes(pantalla, ancho: int, alto: int) -> dict:
    '''
    Devuelve las variables y constantes necesarias para utilizar en funciones de renderizado.
    Recibe la pantalla, el ancho y alto de nuestro juego.
    Retorna un diccionario con las configuraciones.
    '''
    fuente_titulo = pygame.font.Font("assets/fonts/fuentemario.ttf", 30)
    fuente_encabezado = pygame.font.Font("assets/fonts/fuentemario.ttf", 22)
    fuente_puntajes = pygame.font.Font("assets/fonts/fuentemario.ttf", 20)
    fuente_boton = pygame.font.Font("assets/fonts/fuentemario.ttf", 24)

    return {
        "pantalla": pantalla,
        "ancho_pantalla": ancho,
        "alto_pantalla": alto,
        "fuente_puntajes": fuente_puntajes,
        "fuente_titulo": fuente_titulo,
        "fuente_encabezado": fuente_encabezado,
        "fuente_boton": fuente_boton,
        "margen_superior": alto * 0.06,
        "margen_inferior": alto * 0.06,
        "espaciado_renglon": alto * 0.012,
        "inicio_tabla_y": alto * 0.18,
        "color_texto": (50, 50, 50),
        "color_fondo_normal": (250, 250, 255),
        "color_primer_puesto": (255, 223, 100),
        "color_segundo_puesto": (220, 220, 220),
        "color_tercer_puesto": (240, 200, 150),
        "color_encabezado": (180, 220, 255),
        "color_boton_hover": (180, 180, 180),
        "color_boton_normal": (230, 230, 230),
        "color_pantalla_puntaje": (107, 140, 255)
    }


def ejecutar_pantalla_puntajes(ventana, config_puntajes, bandera_musica_fondo):
    '''
    Ejecuta y renderiza la pantalla de puntajes.
    Recibe la ventana principal, la configuracion de variables de esa pantalla y la bandera para saber si el sonido está activo o no.
    Retorna un booleano para saber si se vuelve al menu o no, y el contenido de la bandera del sonido.
    '''
    ventana.fill(config_puntajes["color_pantalla_puntaje"])
    generar_texto_inicial(config_puntajes)
    lista_puntajes = leer_puntajes("assets/files/top_10_users.csv")
    generar_tabla_puntajes(lista_puntajes, config_puntajes)
    rect_boton_volver = generar_boton_volver(config_puntajes)

    bandera_musica_fondo = activar_sonido(bandera_musica_fondo)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            quit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_boton_volver.collidepoint(evento.pos):
                if evento.button == 1:
                    return True, bandera_musica_fondo  

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return True, bandera_musica_fondo  

    return False, bandera_musica_fondo


def generar_texto_inicial(config: dict) -> None:
    """
    Genera y renderiza el texto principal de la pantalla.
    Recibe la config con datos importantes a utilizar para la generación.
    No retorna nada.
    """
    fuente = config["fuente_titulo"]
    ancho_pantalla = config["ancho_pantalla"]
    color_texto = config["color_texto"]
    pantalla = config["pantalla"]
    margen_superior = config["margen_superior"]

    texto_principal = fuente.render(
        "TOP 10 MEJORES PUNTAJES", True, color_texto)
    ancho_texto = texto_principal.get_width()

    posicion_x = (ancho_pantalla - ancho_texto) / 2
    posicion_y = margen_superior

    pantalla.blit(texto_principal, (posicion_x, posicion_y))


def leer_puntajes(ruta_archivo) -> list:
    """
    Lee el archivo CSV con encabezado.
    Devuelve una lista de tuplas con (nombre, puntaje).
    """
    jugadores = []
    encabezado = []

    try:
        with open(ruta_archivo, "r") as archivo:
            lineas = archivo.readlines()

            for i in range(len(lineas)):
                elemento = lineas[i]
                partes = elemento.strip().split(",")

                if len(partes) != 2:
                    continue

                nombre = partes[0]
                puntaje = partes[1]

                if i == 0 and not puntaje.isdigit():
                    encabezado.append( [nombre, puntaje] )
                else:
                    if puntaje.isdigit():
                        jugadores.append( [nombre, int(puntaje)] )

        jugadores.sort(key=lambda x: x[1], reverse=True)

        return encabezado + jugadores

    except FileNotFoundError:
        return []



def generar_tabla_puntajes(lista: list, config: dict) -> None:
    """
    Genera una tabla dentro de la pantalla de puntajes para cada jugador.
    Recibe la informacion o lista de jugadores a mostrar, pygame y un diccionario de variables que necesito para armar la interfaz de la tabla.
    No retorna nada
    """
    fuente_puntajes = config["fuente_puntajes"]
    fuente_encabezado = config["fuente_encabezado"]
    ancho_pantalla = config["ancho_pantalla"]
    alto_pantalla = config["alto_pantalla"]
    pantalla = config["pantalla"]
    inicio_tabla_y = config["inicio_tabla_y"]
    color_texto = config["color_texto"]
    color_fondo_normal = config["color_fondo_normal"]
    color_encabezado = config["color_encabezado"]
    color_primer_puesto = config["color_primer_puesto"]
    color_segundo_puesto = config["color_segundo_puesto"]
    color_tercer_puesto = config["color_tercer_puesto"]

    ancho_renglon = ancho_pantalla * 0.8
    ubicacion_x = (ancho_pantalla - ancho_renglon) / 2

    for i in range(len(lista)):
        fuente = fuente_encabezado if i == 0 else fuente_puntajes

        if i == 1:
            color_fondo = color_primer_puesto
        elif i == 2:
            color_fondo = color_segundo_puesto
        elif i == 3:
            color_fondo = color_tercer_puesto
        elif i % 2 == 0:
            color_fondo = color_fondo_normal
        else:
            color_fondo = (255, 255, 255)

        alto_texto = fuente.get_height()
        alto_renglon = alto_texto + config["espaciado_renglon"]
        ubicacion_y = inicio_tabla_y + (i * (alto_renglon + 5))

        rect = pygame.Rect(ubicacion_x, ubicacion_y,
                           ancho_renglon, alto_renglon)
        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=6)

        texto_pos = "#" if i == 0 else str(i)
        texto_posicion = fuente.render(texto_pos, True, color_texto)
        texto_nombre = fuente.render(
            lista[i][0].upper() if i == 0 else lista[i][0], True, color_texto)
        texto_puntaje = fuente.render(
            lista[i][1].upper() if i == 0 else str(lista[i][1]), True, color_texto)

        pantalla.blit(texto_posicion, texto_posicion.get_rect(
            midleft=(rect.x + 15, rect.centery)))
        pantalla.blit(texto_nombre, texto_nombre.get_rect(
            center=(rect.centerx, rect.centery)))
        pantalla.blit(texto_puntaje, texto_puntaje.get_rect(
            midright=(rect.right - 30, rect.centery)))


def generar_boton_volver(config: dict) -> any:
    """
    Genera el boton para volver al menú principal con su respectivo texto centrado.
    Recibe pygame y un diccionario de configuraciones que me sirven para generar el boton.
    Retorna una surface de pygame.
    """
    mouse_pos = pygame.mouse.get_pos()

    fuente = config["fuente_boton"]
    ancho_pantalla = config["ancho_pantalla"]
    alto_pantalla = config["alto_pantalla"]
    color_texto = config["color_texto"]
    pantalla = config["pantalla"]
    margen_inferior = config["margen_inferior"]
    color_hover = config["color_boton_hover"]
    color_normal = config["color_boton_normal"]

    texto_boton = fuente.render("Volver", True, color_texto)
    ancho_texto = texto_boton.get_width()
    alto_texto = texto_boton.get_height()

    ancho_boton = ancho_texto + ancho_pantalla * 0.05
    alto_boton = alto_texto + alto_pantalla * 0.03
    pos_x = (ancho_pantalla - ancho_boton) / 2
    pos_y = alto_pantalla - alto_boton - margen_inferior

    rect_boton = pygame.Rect(pos_x, pos_y, ancho_boton, alto_boton)
    color_boton = color_hover if rect_boton.collidepoint(
        mouse_pos) else color_normal

    pygame.draw.rect(pantalla, color_boton, rect_boton, border_radius=10)
    pantalla.blit(texto_boton, texto_boton.get_rect(center=rect_boton.center))

    return rect_boton


def activar_sonido(bandera_sonido: str) -> None:
    if bandera_sonido == False:
        pygame.mixer.music.play(-1)
        return True
    
def desactivar_sonido() -> None:
    pygame.mixer.music.stop()
    return True


#########LOGICA DE VICTORIA###########


def definir_penalidad(dificultad: str) -> int:
    '''
    Esta función define el factor a utilizar en el cálculo de puntaje dependiendo la dificultad.
    Recibe la dificultad en string.
    Retorna el factor en entero
    '''
    dificultad = dificultad.lower()

    if dificultad == "facil":
        dificultad_factor = 2000
    elif dificultad == "normal":
        dificultad_factor = 4000
    elif dificultad == "dificil":
        dificultad_factor = 6000
    return dificultad_factor


def calcular_puntaje(dificultad_factor: int, tiempo: int) -> int:
    """
    Calcula el puntaje según el factor de dificultad y tiempo.
    Retorna el puntaje final.
    """
    if tiempo <= 0:
        tiempo = 1

    puntaje = dificultad_factor // tiempo

    return puntaje


def leer_puntajes(ruta_archivo: str) -> list:
    """
    Recibe la ruta del archivo con el nombre del mismo.
    Lee el archivo CSV con encabezado.
    Devuelve una lista de tuplas con (nombre, puntaje).
    """
    jugadores = []
    encabezado = []

    try:
        with open(ruta_archivo, "r") as archivo:
            lineas = archivo.readlines()

            for i in range(len(lineas)):
                elemento = lineas[i]
                partes = elemento.strip().split(",")

                if len(partes) != 2:
                    continue

                nombre = partes[0]
                puntaje = partes[1]

                if i == 0 and not puntaje.isdigit():
                    encabezado.append([nombre, puntaje])
                else:
                    if puntaje.isdigit():
                        jugadores.append([nombre, int(puntaje)])

        jugadores.sort(key=lambda x: x[1], reverse=True)

        return encabezado + jugadores

    except FileNotFoundError:
        return []


def validar_datos_archivo(datos: list, nombre_nuevo: str, puntaje_nuevo: int) -> list:
    """
    Recibe la matriz de datos leida del archivo o lista vacia si no encuentra el archivo, el nombre y puntaje a insertar.
    Devuelve la lista de datos analizados y listos para ingresar al archivo.
    """
    if len(datos) == 0:
        datos = [["nombre", "puntaje"], [nombre_nuevo, puntaje_nuevo]]
    else:
        encontrado = False
        for i in range(1, len(datos)):
            nombre = datos[i][0]
            puntaje = int(datos[i][1])
            if nombre_nuevo == nombre:
                encontrado = True
                if puntaje_nuevo > puntaje:
                    datos[i][1] = puntaje_nuevo
                break
        if encontrado == False:
            datos.append([nombre_nuevo, puntaje_nuevo])

    return datos


def crear_sobreescribir_archivo(datos: list, ruta_archivo: str) -> None:
    """
    Crea o sobreescribe el archivo con los datos nuevos.
    Recibe la matriz de datos extraido del csv y previamente analizadas y la ruta del archivo.
    Retorna None
    """
    with open(ruta_archivo, "w") as archivo:
        for fila in datos:
            archivo.write(f"{fila[0]},{fila[1]}\n")


def obtener_config_cuadro_victoria(pantalla, ancho: int, alto: int) -> dict:
    '''
    Devuelve las variables y constantes necesarias para utilizar en funciones de renderizado.
    Recibe la pantalla, el ancho y alto de nuestro juego.
    Retorna un diccionario con las configuraciones.
    '''

    fuente_titulo = pygame.font.Font("assets/fonts/fuentemario.ttf", 30)
    fuente_encabezado = pygame.font.Font("assets/fonts/fuentemario.ttf", 22)
    fuente_puntajes = pygame.font.Font("assets/fonts/fuentemario.ttf", 20)

    return {
        "pantalla": pantalla,
        "ancho_pantalla": ancho,
        "alto_pantalla": alto,
        "fuente_titulo": fuente_titulo,
        "fuente_encabezado": fuente_encabezado,
        "fuente_puntajes": fuente_puntajes,
        "color_texto": (50, 50, 50),
        "color_fondo_normal": (250, 250, 255),
        "color_pantalla_puntaje": (107, 140, 255),

    }


def renderizar_input_nombre(surface, texto_actual, config, pos_x, pos_y, ancho, alto):
    '''
    Renderiza el input para que el usuario ingrese su nombre.
    Recibe los datos que se mostrarán en pantalla así como también algunas variables no generales sino del propio input.
    Retorna el recuadro surface de pygame.
    '''
    fuente = config["fuente_puntajes"]
    color_texto = config["color_texto"]
    color_fondo = config["color_fondo_normal"]
    color_borde = config["color_pantalla_puntaje"]

    input_rect = pygame.Rect(pos_x, pos_y, ancho, alto)
    pygame.draw.rect(surface, color_fondo, input_rect, border_radius=8)
    pygame.draw.rect(surface, color_borde, input_rect, 3, border_radius=8)

    texto_surface = fuente.render(texto_actual, True, color_texto)
    surface.blit(texto_surface, (input_rect.x + 10, input_rect.y +
                 (alto - texto_surface.get_height()) // 2))

    return input_rect


def renderizar_mensaje_victoria(ventana, rect_cuadro, puntaje, config) -> None:
    '''
    Renderiza el mensaje de victoria y el puntaje a mostrar al usuario antes de que este ingrese su nombre.
    Recibe las configuraciones necesarias.
    Retorna None
    '''
    fuente_titulo = config["fuente_titulo"]
    fuente_puntajes = config["fuente_puntajes"]
    color_texto = config["color_texto"]

    texto_victoria = fuente_titulo.render(
        "¡¡Ganaste!!", True, config["color_pantalla_puntaje"])
    texto_puntaje = fuente_puntajes.render(
        f"Puntaje obtenido: {puntaje}", True, color_texto)
    texto_ingrese = fuente_puntajes.render(
        "Ingrese su nombre:", True, color_texto)

    ventana.blit(texto_victoria, (rect_cuadro.x + 30, rect_cuadro.y + 20))
    ventana.blit(texto_puntaje, (rect_cuadro.x + 30, rect_cuadro.y + 90))
    ventana.blit(texto_ingrese, (rect_cuadro.x + 30, rect_cuadro.y + 140))


def ejecutar_cuadro_victoria(ventana, rect_cuadro, puntaje, config) -> None:
    '''
    Ejecuta y muestra la totalidad del cuadro de victoria.
    Recibe las configuraciones necesarias para el renderizado y el puntaje del usuario.
    Retorna el nombre final del usuario para luego poder guardarlo en un archivo.
    '''
    texto_nombre = ""
    nombre_final = None
    activo = True

    pos_x_input = rect_cuadro.x + 30
    pos_y_input = rect_cuadro.y + 180
    ancho_input = rect_cuadro.width - 60
    alto_input = 50

    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and texto_nombre.strip() != "":
                    nombre_final = texto_nombre.strip()
                    activo = False
                elif event.key == pygame.K_BACKSPACE:
                    texto_nombre = texto_nombre[:-1]
                else:
                    if len(texto_nombre) < 15:
                        texto_nombre += event.unicode

        s = pygame.Surface(
            (config["ancho_pantalla"], config["alto_pantalla"]), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))

        pygame.draw.rect(
            ventana, config["color_fondo_normal"], rect_cuadro, border_radius=15)
        pygame.draw.rect(
            ventana, config["color_pantalla_puntaje"], rect_cuadro, 4, border_radius=15)

        renderizar_mensaje_victoria(ventana, rect_cuadro, puntaje, config)
        renderizar_input_nombre(ventana, texto_nombre, config,
                                pos_x_input, pos_y_input, ancho_input, alto_input)

        pygame.display.flip()

    return nombre_final


def activar_sonido_victoria() -> None:
    '''
    Activa el sonido cuando se necesite.

    '''
    pygame.mixer.music.load("assets/sounds/sonido_victoria.mp3")
    pygame.mixer.music.play(1)


def mostrar_pantalla_victoria(ventana, puntaje, config):
    '''
    Renderiza el componente de victoria completo colocandolo en una posicion adecuada.
    Recibe la ventana de nuestro juego, el puntaje y la config necesaria.
    Retorna el nombre del usuario.
    '''
    activar_sonido_victoria()

    ancho_cuadro = 500
    alto_cuadro = 300
    pos_x_cuadro = config["ancho_pantalla"] // 2 - ancho_cuadro // 2
    pos_y_cuadro = config["alto_pantalla"] // 2 - alto_cuadro // 2
    rect_cuadro = pygame.Rect(
        pos_x_cuadro, pos_y_cuadro, ancho_cuadro, alto_cuadro)

    nombre = ejecutar_cuadro_victoria(ventana, rect_cuadro, puntaje, config)
    return nombre