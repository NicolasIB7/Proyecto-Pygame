def hacer_cadena_timer(segundos: int, minutos: int) -> str:
    '''
    Documentación
    '''
    timer_segundos = f'0{segundos}' if segundos < 10 else f'{segundos}'
    timer_minutos = f'0{minutos}' if minutos < 10 else f'{minutos}'
    return f'{timer_minutos}:{timer_segundos}'