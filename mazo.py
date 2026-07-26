import random
from carta import Carta

class Mazo:
    def __init__(self):
        palos = ['Espada', 'Basto', 'Oro', 'Copa']
        numeros = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
        self.cartas = [Carta(n, p) for p in palos for n in numeros]

    def mezclar(self):
        random.shuffle(self.cartas)

    def repartir(self):
        if len(self.cartas) >= 3:
            return [self.cartas.pop() for _ in range(3)]
        return []