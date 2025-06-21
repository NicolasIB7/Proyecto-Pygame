def obtener_config_puntajes(pygame, pantalla, ancho: int, alto: int) -> dict:

    fuente_titulo = pygame.font.SysFont("Arial", 26)
    fuente_encabezado = pygame.font.SysFont("Arial", 20, bold=True)
    fuente_puntajes = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_boton = pygame.font.SysFont("Arial", 20, bold=True)

    return {
        "pantalla": pantalla,
        "ancho_pantalla": ancho,
        "alto_pantalla": alto,
        "fuente_puntajes": fuente_puntajes,
        "fuente_titulo": fuente_titulo,
        "fuente_encabezado": fuente_encabezado,
        "fuente_boton": fuente_boton,
        "margen_superior": alto * 0.05,
        "margen_inferior": alto * 0.05,
        "espaciado_renglon": alto * 0.01,
        "inicio_tabla_y": alto * 0.15,
        "color_texto": (138, 14, 0),
        "color_fondo_normal": (245, 245, 245),
        "color_primer_puesto": (255, 223, 100),
        "color_segundo_puesto": (220, 220, 220),
        "color_tercer_puesto": (240, 200, 150)
    }


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


def leer_puntajes() -> list:
    """
    Lee el archivo de puntajes CSV generado y los agrupa en lista.
    No recibe nada.
    Retorna una lista de tuplas con el nombre y puntaje de cada jugador.
    """

    # VER DE VALIDAR SI EL SEGUNDO PARAMETRO NO ES UN NUMERO ENTONCES QUIERE DECIR QUE TIENE ENCABEZADO SINO NO
    with open("top_10_users.csv", "r") as archivo:
        lista = archivo.readlines()
        encabezado = []
        jugadores = []

        for renglon in range(len(lista)):
            elemento = lista[renglon]
            if elemento == 0 and elemento[1].isalpha():
                partes = elemento.strip().split(",")
                nombre = partes[0]
                puntaje = partes[1]
                encabezado.append((nombre, puntaje))
            else:
                partes = elemento.strip().split(",")
                nombre = partes[0]
                puntaje = partes[1]
                jugadores.append((nombre, puntaje))

        jugadores.sort(key=lambda x: x[1], reverse=True)

    return encabezado + jugadores


def generar_tabla_puntajes(pygame, lista: list, config: dict) -> None:
    """
    Genera una tabla dentro de la pantalla de puntajes para cada jugador.
    Recibe la informacion o lista de jugadores a mostrar, pygame y un diccionario de variables que necesito para armar la interfaz de la tabla.
    No retorna nada
    """

    fuente_puntajes = config["fuente_puntajes"]
    fuente_encabezado = config["fuente_encabezado"]
    ancho_pantalla = config["ancho_pantalla"]
    alto_pantalla = config["alto_pantalla"]
    color_texto = config["color_texto"]
    pantalla = config["pantalla"]
    inicio_tabla_y = config["inicio_tabla_y"]
    color_primer_puesto = config["color_primer_puesto"]
    color_segundo_puesto = config["color_segundo_puesto"]
    color_tercer_puesto = config["color_tercer_puesto"]
    color_fondo_normal = config["color_fondo_normal"]

    ancho_renglon = ancho_pantalla * 0.8
    ubicacion_x = alto_pantalla * 0.10
    inicio_tabla_puntajes = inicio_tabla_y

    for i in range(len(lista)):

        alto_texto = fuente_encabezado.render(
            lista[i][0], True, color_texto).get_height()

        if i == 0:
            fuente = fuente_encabezado
            color_fondo = (200, 200, 200)
            posicion = fuente_encabezado.render("POSICIÓN", True, color_texto)
            nombre = fuente_encabezado.render(
                lista[i][0].upper(), True, color_texto)
            puntaje = fuente_encabezado.render(
                lista[i][1].upper(), True, color_texto)
        else:
            fuente = fuente_puntajes
            nombre = fuente.render(lista[i][0], True, color_texto)
            puntaje = fuente.render(str(lista[i][1]), True, color_texto)
            posicion = fuente.render(f"{i}.", True, color_texto)

            if i == 1:
                color_fondo = color_primer_puesto
            elif i == 2:
                color_fondo = color_segundo_puesto
            elif i == 3:
                color_fondo = color_tercer_puesto
            else:
                color_fondo = color_fondo_normal

        alto_renglon = alto_texto + alto_pantalla * 0.01
        ubicacion_y = inicio_tabla_puntajes + (i * (alto_renglon + 7))

        rect = pygame.Rect(ubicacion_x, ubicacion_y,
                           ancho_renglon, alto_renglon)
        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=5)

        pantalla.blit(posicion, posicion.get_rect(
            midleft=(rect.x + 15, rect.centery)))
        pantalla.blit(nombre, nombre.get_rect(
            center=(rect.centerx, rect.centery)))
        pantalla.blit(puntaje, puntaje.get_rect(
            midright=(rect.right - 30, rect.centery)))


def generar_boton_volver(pygame, config: dict) -> any:
    """
    Genera el boton para volver al menú principal con su respectivo texto centrado.
    Recibe pygame y un diccionario de configuraciones que me sirven para generar el boton.
    Retorna una surface de pygame.
    """

    fuente = config["fuente_boton"]
    ancho_pantalla = config["ancho_pantalla"]
    alto_pantalla = config["alto_pantalla"]
    color_texto = config["color_texto"]
    pantalla = config["pantalla"]
    margen_inferior = config["margen_inferior"]

    texto_boton = fuente.render("Volver", True, color_texto)
    ancho_texto_boton = texto_boton.get_width()
    alto_texto_boton = texto_boton.get_height()

    boton_volver_ancho = ancho_texto_boton + ancho_pantalla * 0.04
    boton_volver_alto = alto_texto_boton + alto_pantalla * 0.02

    ubicacion_x = (ancho_pantalla - boton_volver_ancho) / 2
    ubicacion_y = alto_pantalla - boton_volver_alto - margen_inferior

    rect_boton_volver = pygame.Rect(
        ubicacion_x, ubicacion_y, boton_volver_ancho, boton_volver_alto)
    texto_boton_centrado = texto_boton.get_rect(
        center=rect_boton_volver.center)

    pygame.draw.rect(pantalla, (230, 230, 230),
                     rect_boton_volver, border_radius=10)
    pantalla.blit(texto_boton, texto_boton_centrado)

    return rect_boton_volver
