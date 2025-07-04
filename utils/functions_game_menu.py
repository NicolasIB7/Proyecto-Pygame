import pygame


def calcular_dimensiones_posicion(pantalla, dim_pos: dict, indice=0) -> tuple:
    '''
    Calcula las dimensiones y posicion de un elemento en una pestaña\n
    pantalla: Superficie que usa para calcular los elementos\n
    dim_pos(dict): Diccionario de donde saca los valores a calcular\n
    indice(int): Indice donde se encuentra los valores del boton en el diccionario\n
    retunr(tuple): retorna una tupla con los valores (x, y, ancho, alto)
    '''
    valores = []
    claves = ('ancho', 'alto', 'x', 'y')

    for i in range(len(dim_pos)):
        if i == indice:
            valores += [{f'{claves[0]}': dim_pos[i][claves[0]], f'{claves[1]}': dim_pos[i][claves[1]],
                         f'{claves[2]}': dim_pos[i][claves[2]], f'{claves[3]}': dim_pos[i][claves[3]]}]

    for i in range(len(valores)):
        ancho_boton = pantalla.get_width() * valores[i]['ancho']
        alto_boton = pantalla.get_height() * valores[i]['alto']
        posicion_x_boton = pantalla.get_width() * valores[i]['x']
        posicion_y_boton = pantalla.get_height() * valores[i]['y']

    return posicion_x_boton, posicion_y_boton, ancho_boton, alto_boton


def crear_buscaminas(pantalla, dic_buscaminas: dict, ancho:int) -> tuple:
    '''
    Crea los valores del cuadro del buscaminas\n
    pantalla: Superficie que usa para calcular los elementos\n
    dic_buscaminas(dict): Diccionario con los valores de buscamias\n
    ancho(int): suma el ancho del elemento mas largo que hay antes del buscaminas
    return(tuple): retorna una tupla con los valores (rectangulo, superficie, lado_sup)
    '''
    lado_sup = int(pantalla.get_height() * dic_buscaminas[0]['dimension'])
    while lado_sup >= (pantalla.get_width() - ancho):
        lado_sup -= 10
    superficie = pygame.Surface((lado_sup, lado_sup))
    superficie.fill("black")

    posicion_x_buscaminas = int(
        pantalla.get_width() * dic_buscaminas[0]['x'] // 2 + ancho)
    posicion_y_buscaminas = int(
        pantalla.get_height()//2 - lado_sup // 2)

    rec_buscaminas = pygame.Rect(
        posicion_x_buscaminas, posicion_y_buscaminas, lado_sup, lado_sup)


    return rec_buscaminas, superficie, lado_sup



# boton

def hacer_boton(pantalla, boton: dict) -> dict:
    """
    Crea los botones de la pantalla\n
    pantalla: Superficie que usa para calcular los elementos\n
    boton(dict): Diccionario con los valores de los botones\n
    return(dict): Retorna un dicionario con las claves ('rectangulo', 'texto', 'posicion', 'imagen')
    """
    botones = []
    for i in range(len(boton)):
        dim_pos = calcular_dimensiones_posicion(pantalla, boton, i)
        rec_boton = pygame.Rect(dim_pos[0], dim_pos[1], dim_pos[2], dim_pos[3])

        imagen_texto_boton = pygame.image.load(boton[i]['texto'])
        imagen_texto_boton = pygame.transform.scale(
            imagen_texto_boton, (rec_boton.width//1.2, rec_boton.height//1.2))
        imagen_rect = imagen_texto_boton.get_rect()
        imagen_rect.center = rec_boton.center
        texto_boton = imagen_texto_boton

        boton_imagen = pygame.image.load(boton[i]['fondo'])
        boton_imagen = pygame.transform.scale(
            boton_imagen, (rec_boton.width, rec_boton.height))

        botones += [{'rectangulo': rec_boton, 'texto': texto_boton,
                     'posicion': imagen_rect, 'imagen': boton_imagen}]

    return botones


def crear_hover_botones(pantalla, dic_boton: dict, texto: list) -> dict:
    '''
    Crea el efecto del hover de un boton\n
    pantalla: Superficie que usa para calcular los elementos\n
    dic_botones: Diccionario de los botones del cual va a hacer su efecto\n
    texto(list): Lista de texto del boton a cambiar para el efecto\n
    return(dict): Retorna un dict del efecto de los botones
    '''
    efecto = 0.002
    hover_botones = []

    for i in range(len(dic_boton)):

        ancho = dic_boton[i]['ancho'] + efecto
        alto = dic_boton[i]['alto'] + efecto
        x = dic_boton[i]['x'] - efecto
        y = dic_boton[i]['y'] - efecto

        for j in range(len(texto)):
            if i == j:
                imagen =  texto[j]

        hover_botones += [ {'ancho': ancho, 'alto': alto, 'x': x, 'y': y, 'texto': imagen,
        'fondo': dic_boton[i]['fondo']}]

    hover_botones = hacer_boton(pantalla, hover_botones)

    return hover_botones


def dibujar_botones(pantalla, dic_botones: dict, dic_hover_botones: dict, mouse_pos: tuple):
    '''
    Dibuja los botones en la pantalla\n
    pantalla: Superficie que usa para calcular los elementos\n
    dic_botones(dict): Botones a dibujar\n
    dic_hover_botones(dict): El efecto hover de los botones\n
    mouse_pos(tuple): posicion actual del mouse
    '''

    for i in range(len(dic_botones)):

        hover = dic_botones[i]['rectangulo'].collidepoint(mouse_pos)

        if hover == True:
            pantalla.blit(
                dic_hover_botones[i]['imagen'], dic_hover_botones[i]['rectangulo'])
            pygame.draw.rect(pantalla, (255, 255, 255),
                             dic_hover_botones[i]['rectangulo'], width=5)
            pantalla.blit(
                dic_hover_botones[i]['texto'], dic_hover_botones[i]['posicion'])
        else:
            pantalla.blit(dic_botones[i]['imagen'],
                          dic_botones[i]['rectangulo'])
            pygame.draw.rect(pantalla, (154, 4, 5),
                             dic_botones[i]['rectangulo'], width=5)
            pantalla.blit(dic_botones[i]['texto'], dic_botones[i]['posicion'])


# contador

def crear_texto_contador(numeros: int = 0) -> str:
    '''
    Crea el texto del contador\n
    numeros(int): Numeros que aparecen en el contador\n
    return(str): Retorna la cadena del contador
    '''
    texto = str(numeros)

    if len(texto) < 3:
        if len(texto) == 1:
            texto = '00' + str(numeros)
        elif len(texto) == 2:
            texto = '0' + str(numeros)
        else:
            texto = str(numeros)

    return texto


def crear_contador(pantalla, dic_contador: dict, contar: int) -> tuple:
    '''
    Crea un contador con su posicion en pantalla\n
    pantalla: Superficie que usa para calcular los elementos\n
    dic_contador(dict): dict con los valores del contador\n
    return(tuple): Retorna una tupla con los valores (rectangulo, pocision de texto, texto)
    '''
    dim_pos = calcular_dimensiones_posicion(pantalla, dic_contador)
    rec_contador = pygame.Rect(dim_pos[0], dim_pos[1], dim_pos[2], dim_pos[3])

    superficie = pygame.Surface((dim_pos[2], dim_pos[3]))
    tamaño_fuente = int(superficie.get_width() * dic_contador[0]['fuente'])
    fuente = pygame.font.SysFont('freesansbold', tamaño_fuente)

    texto = fuente.render(crear_texto_contador(contar), True, (255, 0, 0))
    posicion_texto = texto.get_rect(center=rec_contador.center)

    return rec_contador, posicion_texto, texto


# timer

def hacer_cadena_timer(tiempo: tuple[int] = (0, 0)) -> str:
    """
    Crea la cadena de (minutos/segundos) del timer\n
    tiempo(tuple[int]): Tupla de minutos y segundo\n
    return(str): Retorna una cadena de 3 digitos del contador
    """
    timer_segundos = f'{tiempo[1]}'
    timer_minutos = f'{tiempo[0]}'

    if tiempo[1] < 10:
        timer_segundos = '0' + f'{tiempo[1]}'

    if tiempo[0] < 10:
        timer_minutos = '0' + f'{tiempo[0]}'

    cadena = f'{timer_minutos}:{timer_segundos}'

    return cadena


def crear_timer(pantalla, timer: dict) -> tuple:
    '''
    Crea un timer en minutos y segundos\n
    pantalla: Superficie que usa para calcular los elementos\n
    timer(dict): Valores del timerque usa para calcular\n
    return(tuple): Retorna una tupla con (texto del timer, cuadro del timer, evento_segundos, rec del texto)
    '''
    evento_segundo = pygame.USEREVENT + 1
    pygame.time.set_timer(evento_segundo, 1000)

    dim_pos = calcular_dimensiones_posicion(pantalla, timer)
    cuadro_timer = pygame.Rect(dim_pos[0], dim_pos[1], dim_pos[2], dim_pos[3])

    tamaño_fuente_timer = int(
        ((timer[0]['fuente']*pantalla.get_width())/800 + (timer[0]['fuente']*pantalla.get_height())/600)/2)

    fuente = pygame.font.SysFont('freesansbold', tamaño_fuente_timer)

    texto_timer = fuente.render(hacer_cadena_timer(
        timer[0]['texto']), True, timer[0]['color'])
    texto_rect = texto_timer.get_rect(center=cuadro_timer.center)

    return texto_timer, cuadro_timer, evento_segundo, texto_rect


def dibujar_elementos_pantalla(pantalla, elementos: dict, COLOR_RECTANGULOS: tuple, mouse_pos: tuple):
    '''
    Dibuja los elementos en la pantalla\n
    pantalla: Superficie que usa para calcular los elementos\n
    elementos(dict): Valores de los elementos a dibujar en pantalla\n
    color_rectangulos(tuple): El color de fondo del contador y timer\n
    mause_pos(tuple): posicion actual del mouse
    '''
    # bucaminas
    pantalla.blit(elementos[0]['buscaminas'][1], elementos[0]['buscaminas'][0])
    pygame.draw.rect(pantalla, COLOR_RECTANGULOS,
                     elementos[0]['buscaminas'][0])

    # timer
    pygame.draw.rect(pantalla, COLOR_RECTANGULOS,
                     elementos[0]['timer'][1], border_radius=15)
    pygame.draw.rect(pantalla, (232, 216, 67),
                     elementos[0]['timer'][1], width=5, border_radius=15)
    pantalla.blit(elementos[0]['timer'][0], elementos[0]['timer'][3])

    # contador
    pygame.draw.rect(pantalla, COLOR_RECTANGULOS,
                     elementos[0]['contador'][0], border_radius=20)
    pygame.draw.rect(pantalla, (230, 16, 73),
                     elementos[0]['contador'][0], width=5, border_radius=20)
    pantalla.blit(elementos[0]['contador'][2], elementos[0]['contador'][1])

    # botones
    dibujar_botones(
        pantalla, elementos[0]['botones'], elementos[0]['hover'], mouse_pos)


def dibujar_pantalla_dif(pantalla, imagenes: dict, fondo: str):
    '''
    Dibuja el fondo con un titulo y/o titulos de los botones\n
    pantalla: Pantalla donde va a dibujar\n
    imagenes(dict): los titulos que dibuja\n
    fondo(str): ruta del fondo que va a dibujar
    '''
    pantalla_rect = imagenes[0]['superficie'].get_rect()

    fondo_pantall_dificultad = pygame.image.load(fondo)
    fondo_pantall_dificultad = pygame.transform.scale(
        fondo_pantall_dificultad, (pantalla_rect.width, pantalla_rect.height))
    pantalla.blit(fondo_pantall_dificultad, (0, 0))
    for i in range(len(imagenes)):

        if imagenes[i]['rect'] == 'pantalla':
            imagen_texto_boton = pygame.image.load(imagenes[i]['titulo'])
            imagen_texto_boton = pygame.transform.scale(
                imagen_texto_boton, (pantalla_rect.width//1.2, pantalla_rect.height//3.5))
            imagen_rect = imagen_texto_boton.get_rect(
                center=(pantalla_rect.centerx + 15, pantalla_rect.centery -  (pantalla_rect.height//3.50)))
        else:
            imagen_texto_boton = pygame.image.load(imagenes[i]['titulo'])
            imagen_texto_boton = pygame.transform.scale(imagen_texto_boton, (
                imagenes[i]['superficie'].width//1.2, imagenes[i]['superficie'].height//1.85))
            imagen_rect = imagen_texto_boton.get_rect(center=(
                imagenes[i]['superficie'].centerx, imagenes[i]['superficie'].centery - (imagenes[i]['superficie'].height/1.3)))

        pantalla.blit(imagen_texto_boton, imagen_rect)


def inicializar_matriz_por_dificultad(dificultad: str, diccionario: dict, ancho_buscaminas: int, CUBIERTA) -> tuple:
    '''
    Inicializa matrices y parámetros de juego según la dificultad elegida
    dificultad(str): clave de dificultad (facil/normal/dificil)
    diccionario(dict): lista de valores de dificultad
    ancho_buscaminas(int): ancho del área del buscaminas
    return:
        matriz_estado
        matriz_juego
        columnas
        minas
        tamaño_celda
    '''
    for config in diccionario:
        if config['dificultad'] == dificultad:
            columnas = config['columnas']
            minas = config['minas']
            break

    matriz_estado = []
    for _ in range(columnas):
        fila = []
        for _ in range(columnas):
            fila.append(CUBIERTA)
        matriz_estado.append(fila)

    matriz_juego = []
    for _ in range(columnas):
        fila = []
        for _ in range(columnas):
            fila.append(0)
        matriz_juego.append(fila)

    tamaño_celda = int(ancho_buscaminas // columnas)

    return matriz_estado, matriz_juego, columnas, minas, tamaño_celda


def reiniciar_juego(ventana, minas, fuente, dic_contador, dic_timer, columnas, filas, color_timer_numeros, CUBIERTA):
    banderas_colocadas = 0
    contador = crear_contador(ventana, dic_contador, minas)
    BUSCAMINAS_INICIADO = False
    timer_segundos = 0
    timer_minutos = 0
    dic_timer[0]['texto'] = [timer_minutos, timer_segundos]
    timer = crear_timer(ventana, dic_timer)
    texto_timer = fuente.render("00:00", True, color_timer_numeros)

    matriz_estado = []
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(CUBIERTA)
        matriz_estado.append(fila)

    matriz_juego = []
    for _ in range(filas):
        fila = []
        for _ in range(columnas):
            fila.append(0)
        matriz_juego.append(fila)

    primera_jugada = True
    estado_derrota = False
    celda_explotada = None

    return (
        banderas_colocadas, contador, BUSCAMINAS_INICIADO,
        timer_segundos, timer_minutos, dic_timer, timer, texto_timer,
        matriz_estado, matriz_juego, primera_jugada, estado_derrota, celda_explotada
    )


def procesar_dificultad(
    dificultad,
    dic_valores_dif,
    buscaminas_width,
    cubierto_constante,
    ventana,
    dic_contador
):
    """
    Configura todo según la dificultad elegida.
    Retorna:
    - matriz_estado
    - matriz_juego
    - columnas
    - minas
    - tamaño_celda
    - imagen_mina
    - imagen_bandera
    - contador
    """

    (matriz_estado, matriz_juego, columnas, minas, tamaño_celda) = inicializar_matriz_por_dificultad(
        dificultad,
        dic_valores_dif,
        buscaminas_width,
        cubierto_constante
    )

    tamaño_celda = float(buscaminas_width / columnas)

    imagen_mina = pygame.transform.scale(
        pygame.image.load("assets/images/imagen_mina.png"),
        (tamaño_celda, tamaño_celda)
    )

    imagen_bandera = pygame.transform.scale(
        pygame.image.load("assets/images/imagen_bandera.png"),
        (tamaño_celda, tamaño_celda)
    )

    contador = crear_contador(ventana, dic_contador, minas)

    return (
        matriz_estado, matriz_juego, columnas, minas, tamaño_celda,
        imagen_mina, imagen_bandera, contador
    )
