from mazo import Mazo
from jugador import Jugador
from reglas import calcular_envido, determinar_ganador_mano

def iniciar_partida():
    jugador1 = Jugador("Vos")
    jugador2 = Jugador("Computadora")
    
    puntos_j1 = 0
    puntos_j2 = 0
    sos_mano = True # Alterna cada ronda completa
    
    while puntos_j1 < 30 and puntos_j2 < 30:
        print("\n" + "="*50)
        print(f"MARCADOR: {jugador1.nombre} [{puntos_j1}] - {jugador2.nombre} [{puntos_j2}]")
        print("="*50 + "\n")
        
        mazo = Mazo()
        mazo.mezclar()
        jugador1.recibir_cartas(mazo.repartir())
        jugador2.recibir_cartas(mazo.repartir())
        
        puntos_ronda = 1 
        manos_j1 = 0
        manos_j2 = 0
        ganador_primera = None
        resultado_anterior = None # Para saber quién tira primero en la mano 2 y 3
        
        envido_cantado = False
        truco_cantado = False
        ronda_terminada = False
        
        print("=== NUEVA RONDA ===")
        print(f">> Tu Envido oculto es: {jugador1.obtener_puntos_envido()} puntos\n")

        for turno in range(1, 4):
            if ronda_terminada: break
            
            print(f"\n--- MANO {turno} ---")
            jugador1.mostrar_mano()
            
            carta_j1 = None
            carta_j2 = None
            
            # Definir quién tiene el turno inicial en esta mano específica
            if turno == 1:
                juega_j1_primero = sos_mano
            else:
                if resultado_anterior == 1: juega_j1_primero = True
                elif resultado_anterior == 2: juega_j1_primero = False
                else: juega_j1_primero = sos_mano # Si fue parda, mantiene el que era mano

            # ----------------------------------------------------
            # ESCENARIO A: VOS TIRÁS PRIMERO
            # ----------------------------------------------------
            if juega_j1_primero:
                carta_jugada = False
                while not carta_jugada and not ronda_terminada:
                    menu = "\nAcciones: [0, 1, 2] tirar carta"
                    if not truco_cantado: menu += " | [T] Truco"
                    if turno == 1 and not envido_cantado: menu += " | [E] Envido"
                    
                    accion = input(menu + "\n¿Qué hacés?: ").strip().upper()
                    
                    if accion == 'T' and not truco_cantado:
                        print(f"\n{jugador1.nombre}: ¡TRUCO!")
                        truco_cantado = True
                        if max([c.valor_truco for c in jugador2.mano]) >= 9:
                            print(f"{jugador2.nombre}: ¡Quiero!")
                            puntos_ronda = 2
                        else:
                            print(f"{jugador2.nombre}: No quiero.")
                            puntos_j1 += 1
                            ronda_terminada = True
                    
                    elif accion == 'E' and turno == 1 and not envido_cantado:
                        print(f"\n{jugador1.nombre}: ¡ENVIDO!")
                        envido_cantado = True
                        env_j2 = jugador2.obtener_puntos_envido()
                        if env_j2 >= 23:
                            print(f"{jugador2.nombre}: ¡Quiero!")
                            env_j1 = jugador1.obtener_puntos_envido()
                            print(f"Tus tantos: {env_j1} | PC: {env_j2}")
                            if env_j1 >= env_j2: puntos_j1 += 2; print("¡Ganaste 2 pts!")
                            else: puntos_j2 += 2; print("La PC gana 2 pts.")
                        else:
                            print(f"{jugador2.nombre}: No quiero.")
                            puntos_j1 += 1
                            
                    elif accion in ['0', '1', '2']:
                        indice = int(accion)
                        if 0 <= indice < len(jugador1.mano):
                            carta_j1 = jugador1.jugar_carta(indice)
                            carta_jugada = True
                        else: print("Carta ya jugada.")
                
                if ronda_terminada: break

                # La PC responde a tu carta
                cartas_ganadoras = [c for c in jugador2.mano if c.valor_truco > carta_j1.valor_truco]
                carta_elegida = min(cartas_ganadoras, key=lambda c: c.valor_truco) if cartas_ganadoras else min(jugador2.mano, key=lambda c: c.valor_truco)
                carta_j2 = jugador2.jugar_carta(jugador2.mano.index(carta_elegida))

            # ----------------------------------------------------
            # ESCENARIO B: LA PC TIRA PRIMERO
            # ----------------------------------------------------
            else:
                # 1. La PC canta Envido si es turno 1 y tiene buenos puntos
                if turno == 1 and not envido_cantado:
                    if jugador2.obtener_puntos_envido() >= 25:
                        print(f"\n¡{jugador2.nombre} canta ENVIDO!")
                        envido_cantado = True
                        resp = input("¿[Q] Quiero o [N] No quiero?: ").strip().upper()
                        if resp == 'Q':
                            env_j1 = jugador1.obtener_puntos_envido()
                            env_j2 = jugador2.obtener_puntos_envido()
                            print(f"Tus tantos: {env_j1} | PC: {env_j2}")
                            if env_j1 >= env_j2: puntos_j1 += 2; print("¡Ganaste 2 pts!")
                            else: puntos_j2 += 2; print("La PC gana 2 pts.")
                        else:
                            puntos_j2 += 1
                            print("Te achicaste. La PC suma 1 pt.")
                
                # La PC tira su mejor carta para presionarte
                carta_elegida = max(jugador2.mano, key=lambda c: c.valor_truco)
                carta_j2 = jugador2.jugar_carta(jugador2.mano.index(carta_elegida))
                print(f"\n> {jugador2.nombre} tira a la mesa: {carta_j2} (Peso: {carta_j2.valor_truco})")
                
                # Tu turno para responder (podés cantar Truco antes de tirar)
                carta_jugada = False
                while not carta_jugada and not ronda_terminada:
                    menu = "\nLa PC ya tiró. Acciones: [0, 1, 2] responder carta"
                    if not truco_cantado: menu += " | [T] Truco"
                    
                    accion = input(menu + "\n¿Qué hacés?: ").strip().upper()
                    
                    if accion == 'T' and not truco_cantado:
                        print(f"\n{jugador1.nombre}: ¡TRUCO!")
                        truco_cantado = True
                        if max([c.valor_truco for c in jugador2.mano]) >= 9 or carta_j2.valor_truco >= 10:
                            print(f"{jugador2.nombre}: ¡Quiero!")
                            puntos_ronda = 2
                        else:
                            print(f"{jugador2.nombre}: No quiero.")
                            puntos_j1 += 1
                            ronda_terminada = True
                            
                    elif accion in ['0', '1', '2']:
                        indice = int(accion)
                        if 0 <= indice < len(jugador1.mano):
                            carta_j1 = jugador1.jugar_carta(indice)
                            carta_jugada = True
                        else: print("Carta ya jugada.")

            # ----------------------------------------------------
            # RESOLUCIÓN DE LA TIRADA
            # ----------------------------------------------------
            if ronda_terminada: break
            
            print(f"\n> VOS: {carta_j1} (Peso: {carta_j1.valor_truco})")
            print(f"> PC : {carta_j2} (Peso: {carta_j2.valor_truco})")
            
            resultado = determinar_ganador_mano(carta_j1, carta_j2)
            resultado_anterior = resultado # Lo guardamos para saber quién arranca la próxima
            
            if resultado == 1:
                print(f"¡Ganaste la mano {turno}!")
                manos_j1 += 1
                if turno == 1: ganador_primera = 1
            elif resultado == 2:
                print(f"¡La PC ganó la mano {turno}!")
                manos_j2 += 1
                if turno == 1: ganador_primera = 2
            else:
                print("¡Es Parda!")
                if turno == 1: ganador_primera = 0
            
            # Evaluación del ganador de la ronda
            if manos_j1 == 2 or (resultado == 0 and turno > 1 and ganador_primera == 1):
                print(f"🏆 ¡Ganaste la ronda! Sumás {puntos_ronda} puntos.")
                puntos_j1 += puntos_ronda
                break
            elif manos_j2 == 2 or (resultado == 0 and turno > 1 and ganador_primera == 2):
                print(f"💀 La PC ganó la ronda. Suma {puntos_ronda} puntos.")
                puntos_j2 += puntos_ronda
                break
            elif resultado == 0 and turno == 3 and ganador_primera == 0:
                ganador = jugador1.nombre if sos_mano else jugador2.nombre
                print(f"🏆 ¡Ganó {ganador} la ronda por ser mano! Suma {puntos_ronda} pts.")
                if sos_mano: puntos_j1 += puntos_ronda
                else: puntos_j2 += puntos_ronda
                break
        
        sos_mano = not sos_mano # Cambio de repartidor para la nueva ronda

if __name__ == "__main__":
    iniciar_partida()