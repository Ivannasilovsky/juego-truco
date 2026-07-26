from reglas import calcular_envido

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
        self.puntos = 0

    def recibir_cartas(self, cartas):
        self.mano = cartas

    def jugar_carta(self, indice):
        # Saca la carta de la mano (usando pop) y la tira a la mesa
        if 0 <= indice < len(self.mano):
            return self.mano.pop(indice)
        return None

    def obtener_puntos_envido(self):
        # El jugador usa la regla del envido sobre las cartas que tiene en la mano
        return calcular_envido(self.mano)

    def mostrar_mano(self):
        print(f"--- Mano de {self.nombre} ---")
        for i, carta in enumerate(self.mano):
            # Le agregamos el 'valor_truco' para que veas el peso de la carta.
            # Recordá: 14 es el Ancho de Espadas (la más fuerte) y 1 es el Cuatro (la más débil).
            print(f"[{i}] {carta} (Peso: {carta.valor_truco})")