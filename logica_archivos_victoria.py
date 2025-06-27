import pygame

# TERMINAR DE AJUSTAR CON CONSTANTES REALES


def renderizar_input_nombre(surface, texto_actual, pos_x=150, pos_y=150, ancho=300, alto=50):
    """
    Recibe
    Crea un cuadro de texto sobre una pantalla ya creada.
    Devuelve el rect para poder colisionarlo y transformarlo en input.
    """
    NEGRO = (0, 0, 0)
    GRIS = (200, 200, 200)
    fuente = pygame.font.SysFont(None, 40)

    input_rect = pygame.Rect(pos_x, pos_y, ancho, alto)

    pygame.draw.rect(surface, GRIS, input_rect, 2)

    texto_surface = fuente.render(texto_actual, True, NEGRO)
    surface.blit(texto_surface, (input_rect.x + 5, input_rect.y + 5))

    return input_rect


def ejecutar_input_usuario(ventana):
    '''
    Utiliza elementos de colision de pygame para escuchar eventos del usuario con teclado.
    Recibe la ventana de nuestro juego.
    Retorna el nombre ingresado.
    '''
    texto_nombre = ""
    nombre_final = None
    activo = True

    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    nombre_final = texto_nombre
                    activo = False
                elif event.key == pygame.K_BACKSPACE:
                    texto_nombre = texto_nombre[:-1]
                else:
                    texto_nombre += event.unicode

        ventana.fill((255, 255, 255))

        renderizar_input_nombre(ventana, texto_nombre)

        pygame.display.flip()

    return nombre_final


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

# VERIFICAR QUE TIEMPO ME PASARA O COMO SE GUARDA EL TIEMPO EN PANTALLA PRINCIPAL


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
