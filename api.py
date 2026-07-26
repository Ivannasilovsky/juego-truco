from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from mazo import Mazo
from jugador import Jugador
from reglas import determinar_ganador_mano

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado global con la memoria de la partida
estado_partida = {
    "puntos_j1": 0,
    "puntos_j2": 0,
    "jugador1": None,
    "jugador2": None,
    "manos_j1": 0,
    "manos_j2": 0,
    "puntos_ronda": 1,
    "envido_cantado": False,
    "truco_cantado": False,
    "turno_actual": 1
}

# El modelo ahora acepta una acción opcional (ej: 'E' para Envido, 'T' para Truco)
class Jugada(BaseModel):
    indice_carta: int = -1
    accion: str = "TIRAR" # "TIRAR", "ENVIDO", "TRUCO"

@app.get("/repartir")
def repartir_mano():
    estado_partida["manos_j1"] = 0
    estado_partida["manos_j2"] = 0
    estado_partida["puntos_ronda"] = 1
    estado_partida["envido_cantado"] = False
    estado_partida["truco_cantado"] = False
    estado_partida["turno_actual"] = 1
    
    estado_partida["jugador1"] = Jugador("Vos")
    estado_partida["jugador2"] = Jugador("PC")
    
    mazo = Mazo()
    mazo.mezclar()
    
    # ... código de repartir ...
    estado_partida["jugador1"].recibir_cartas(mazo.repartir())
    estado_partida["jugador2"].recibir_cartas(mazo.repartir())
    
    # Reemplazamos la vieja lista por una que incluye el peso (valor_truco)
    cartas_info = [{"nombre": f"{c.numero} de {c.palo}", "peso": c.valor_truco} for c in estado_partida["jugador1"].mano]
    
    tantos_j1 = estado_partida["jugador1"].obtener_puntos_envido()
    
    return {
        "puntos_j1": estado_partida["puntos_j1"],
        "puntos_j2": estado_partida["puntos_j2"],
        "cartas_recibidas": cartas_info, # <- Ahora mandamos la info completa
        "tantos_envido": tantos_j1
    }

@app.post("/jugar_carta")
def jugar_carta(jugada: Jugada):
    j1 = estado_partida["jugador1"]
    j2 = estado_partida["jugador2"]
    
    # -----------------------------------------------------------
    # CANTO DE ENVIDO
    # -----------------------------------------------------------
    if jugada.accion == "ENVIDO":
        estado_partida["envido_cantado"] = True
        env_j2 = j2.obtener_puntos_envido()
        
        if env_j2 >= 23:
            env_j1 = j1.obtener_puntos_envido()
            if env_j1 >= env_j2:
                estado_partida["puntos_j1"] += 2
                msg = f"PC: ¡Quiero! Tus tantos: {env_j1} | PC: {env_j2}. ¡Ganaste el Envido (+2 pts)!"
            else:
                estado_partida["puntos_j2"] += 2
                msg = f"PC: ¡Quiero! Tus tantos: {env_j1} | PC: {env_j2}. La PC gana el Envido (+2 pts)."
        else:
            estado_partida["puntos_j1"] += 1
            msg = f"PC: No quiero. Ganás 1 punto por el Envido."
            
        return {
            "es_canto": True,
            "mensaje_canto": msg,
            "puntos_j1": estado_partida["puntos_j1"],
            "puntos_j2": estado_partida["puntos_j2"],
            "envido_cantado": True,
            "truco_cantado": estado_partida["truco_cantado"]
        }

    # -----------------------------------------------------------
    # CANTO DE TRUCO
    # -----------------------------------------------------------
    if jugada.accion == "TRUCO":
        estado_partida["truco_cantado"] = True
        mejor_carta_pc = max([c.valor_truco for c in j2.mano]) if j2.mano else 0
        
        if mejor_carta_pc >= 9:
            estado_partida["puntos_ronda"] = 2
            msg = "PC: ¡Quiero! El Truco está en juego por 2 puntos."
            return {
                "es_canto": True,
                "mensaje_canto": msg,
                "puntos_j1": estado_partida["puntos_j1"],
                "puntos_j2": estado_partida["puntos_j2"],
                "envido_cantado": estado_partida["envido_cantado"],
                "truco_cantado": True
            }
        else:
            estado_partida["puntos_j1"] += 1
            msg = "PC: No quiero. ¡Se achicó! Ganás la ronda (+1 pt)."
            return {
                "es_canto": True,
                "mensaje_canto": msg,
                "ronda_terminada": True,
                "puntos_j1": estado_partida["puntos_j1"],
                "puntos_j2": estado_partida["puntos_j2"]
            }

    # -----------------------------------------------------------
    # JUGADA NORMAL (Tirar carta)
    # -----------------------------------------------------------
    carta_j1 = j1.jugar_carta(jugada.indice_carta)
    
    cartas_ganadoras = [c for c in j2.mano if c.valor_truco > carta_j1.valor_truco]
    carta_elegida = min(cartas_ganadoras, key=lambda c: c.valor_truco) if cartas_ganadoras else min(j2.mano, key=lambda c: c.valor_truco)
    carta_j2 = j2.jugar_carta(j2.mano.index(carta_elegida))
    
    resultado = determinar_ganador_mano(carta_j1, carta_j2)
    
    mensaje_mano = ""
    if resultado == 1:
        estado_partida["manos_j1"] += 1
        mensaje_mano = "¡Ganaste esta mano!"
    elif resultado == 2:
        estado_partida["manos_j2"] += 1
        mensaje_mano = "La PC ganó esta mano."
    else:
        mensaje_mano = "¡Es parda!"
    
    ronda_terminada = False
    mensaje_ronda = ""
    pts = estado_partida["puntos_ronda"]
    
    if estado_partida["manos_j1"] >= 2:
        estado_partida["puntos_j1"] += pts
        mensaje_ronda = f"🏆 ¡Ganaste la ronda! Sumás {pts} pt(s)."
        ronda_terminada = True
    elif estado_partida["manos_j2"] >= 2:
        estado_partida["puntos_j2"] += pts
        mensaje_ronda = f"💀 La PC ganó la ronda. Suma {pts} pt(s)."
        ronda_terminada = True
        
    estado_partida["turno_actual"] += 1
    
    return {
        "es_canto": False,
        "carta_tuya": f"{carta_j1.numero} de {carta_j1.palo}",
        "carta_pc": f"{carta_j2.numero} de {carta_j2.palo}",
        "mensaje_mano": mensaje_mano,
        "ronda_terminada": ronda_terminada,
        "mensaje_ronda": mensaje_ronda,
        "puntos_j1": estado_partida["puntos_j1"],
        "puntos_j2": estado_partida["puntos_j2"],
        "turno_actual": estado_partida["turno_actual"]
    }