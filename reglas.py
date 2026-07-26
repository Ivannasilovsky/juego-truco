def calcular_envido(mano):
    #agrupamos los valores de las cartas segun su palo
    cartas_por_palo = {}
    for carta in mano:
        cartas_por_palo.setdefault(carta.palo, []).append(carta.valor_envido)
    
    puntos_posibles = []
    
    for palo, valores in cartas_por_palo.items():
        if len(valores) >= 2:
            #si hay 2 0 3 cartas del mismo palo, sumamos 20 + las dos mas altas
            valores.sort(reverse=True)
            puntos_posibles.append(20 + valores[0] + valores[1])
        
        else:
            #si es una sola carta, el posible punto es solo un valor base
            puntos_posibles.append(valores[0])
        
    return max(puntos_posibles)

def determinar_ganador_mano(carta_jugador1, carta_jugador2):
    """
    Compara dos cartas usando su jerarquía de truco.
    Devuelve 1 (Gana J1), 2 (Gana J2) o 0 (Parda).
    """
    if carta_jugador1.valor_truco > carta_jugador2.valor_truco:
        return 1
    elif carta_jugador2.valor_truco > carta_jugador1.valor_truco:
        return 2
    else:
        # Tienen el mismo valor (ej: un 3 de Copa y un 3 de Basto)
        return 0