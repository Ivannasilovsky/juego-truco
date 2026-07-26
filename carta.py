class Carta:
    def __init__(self, numero, palo):
        self.numero = numero
        self.palo = palo
        self.valor_envido = self._calcular_envido()
        self.valor_truco = self._calcular_truco()

    def _calcular_envido(self):
        if self.numero in [10, 11, 12]:
            return 0
        return self.numero

    def _calcular_truco(self):
        if self.numero == 1 and self.palo == 'Espada': return 14
        if self.numero == 1 and self.palo == 'Basto': return 13
        if self.numero == 7 and self.palo == 'Espada': return 12
        if self.numero == 7 and self.palo == 'Oro': return 11
        
        if self.numero == 3: return 10
        if self.numero == 2: return 9
        if self.numero == 1 and self.palo in ['Copa', 'Oro']: return 8
        
        if self.numero == 12: return 7
        if self.numero == 11: return 6
        if self.numero == 10: return 5
        if self.numero == 7 and self.palo in ['Copa', 'Basto']: return 4
        if self.numero == 6: return 3
        if self.numero == 5: return 2
        if self.numero == 4: return 1
        return 0

    def __str__(self):
        return f"{self.numero} de {self.palo}"
    
    def __repr__(self):
        return self.__str__()