import pygame


def definir_penalidad(dificultad: str) -> int:
    '''
    Esta función define el factor a utilizar en el cálculo de puntaje dependiendo la dificultad.
    Recibe la dificultad en string.
    Retorna el factor en entero
    '''
    dificultad = dificultad.lower()

    if dificultad == "facil":
        dificultad_factor = 2000
    elif dificultad == "medio":
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


#EJEMPLO DE EJECUCION CUANDO SE GANA: 

        # config_victoria = obtener_config_cuadro_victoria(ventana, ANCHO, ALTO)

        # puntaje = 200
        # nombre_usuario = mostrar_pantalla_victoria(ventana, puntaje, config_victoria)
        # penalidad = definir_penalidad("Medio")
        # puntaje_final = calcular_puntaje(penalidad, puntaje)
        # datos = leer_puntajes("top_10.csv")
        # datos_finales = validar_datos_archivo(datos, nombre_usuario, puntaje_final)
        # crear_sobreescribir_archivo(datos_finales, "top_10.csv")
        # pantalla_prueba = False
        # pantalla_principal = True