import numpy as np

from model import WECswarm


class Ocean:
    def __init__(self, width=100, height=100, power:int = 1):
        self.width = width
        self.height = height
        self.max_power = power
        self.data = np.ones((self.width, self.height))*self.max_power
        self.data[(1, 1)] = 0
        self.data[(0, 1)] = 3

    def bilinear_interpolation(self, pos):
        """
        Interpolazione bilineare del campo 2D 'field' alla posizione continua (x, y).
        Ritorna un valore float compreso tra 0 e 1.
        """
        x = pos[0]
        y = pos[1]
        x0 = int(np.floor(x))
        x1 = x0 + 1

        y0 = int(np.floor(y))
        y1 = y0 + 1

        # Frazioni tra i due punti (quanto è vicino a x0 rispetto a x1, ecc.)
        dx = x - x0
        dy = y - y0

        # Valori nei 4 angoli
        Q11 = self.data[x0, y0]
        Q21 = self.data[x0, y1]
        Q12 = self.data[x1, y0]
        Q22 = self.data[x1, y1]

        # Interpolazione bilineare
        value = value = (
        Q11 * (1 - dx) * (1 - dy) +
        Q21 * dx * (1 - dy) +
        Q12 * (1 - dx) * dy +
        Q22 * dx * dy
        )
        return value

    def get_power(self, pos):
        power = self.bilinear_interpolation(pos=pos)
        print(power)
        return power




Ocean.get_power(pos=(0.5, 0.5))