def obtener_config_puntajes(pygame, pantalla, ancho: int, alto: int) -> dict:
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
        "color_boton_normal": (230, 230, 230)
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

    texto_principal = fuente.render("TOP 10 MEJORES PUNTAJES", True, color_texto)
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
    with open("assets/files/top_10_users.csv", "r") as archivo:
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
        elif i%2 == 0:
            color_fondo = color_fondo_normal
        else:
            color_fondo = (255, 255, 255)
            
        alto_texto = fuente.get_height()
        alto_renglon = alto_texto + config["espaciado_renglon"]
        ubicacion_y = inicio_tabla_y + (i * (alto_renglon + 5))

        rect = pygame.Rect(ubicacion_x, ubicacion_y, ancho_renglon, alto_renglon)
        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=6)

        texto_pos = "#" if i == 0 else str(i)
        texto_posicion = fuente.render(texto_pos, True, color_texto)
        texto_nombre = fuente.render(lista[i][0].upper() if i == 0 else lista[i][0], True, color_texto)
        texto_puntaje = fuente.render(lista[i][1].upper() if i == 0 else str(lista[i][1]), True, color_texto)

        pantalla.blit(texto_posicion, texto_posicion.get_rect(midleft=(rect.x + 15, rect.centery)))
        pantalla.blit(texto_nombre, texto_nombre.get_rect(center=(rect.centerx, rect.centery)))
        pantalla.blit(texto_puntaje, texto_puntaje.get_rect(midright=(rect.right - 30, rect.centery)))

def generar_boton_volver(pygame, config: dict) -> any:
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
    color_boton = color_hover if rect_boton.collidepoint(mouse_pos) else color_normal

    pygame.draw.rect(pantalla, color_boton, rect_boton, border_radius=10)
    pantalla.blit(texto_boton, texto_boton.get_rect(center=rect_boton.center))

    return rect_boton
