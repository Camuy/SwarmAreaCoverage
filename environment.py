import numpy as np
from scipy.ndimage import gaussian_filter
from matplotlib import pyplot as plt

from mesa.space import PropertyLayer




class Ocean(PropertyLayer):
    def __init__(self, width: int = 100, height: int = 100, max_power:int = 1):
        super().__init__(name="Ocean", width=width, height=height, default_value=1)
        self.width = width
        self.height = height
        self.max_power = max_power
        # self.power = self.create_env()
        self.sigma = 15


    def modify_ocean(self):
        rand_power = np.random.rand(self.width, self.height)
        power_distribution = gaussian_filter(rand_power, sigma=self.sigma)  # più sigma = più liscio
        norm = np.dot(np.divide(power_distribution - np.min(power_distribution), np.max(power_distribution) - np.min(power_distribution)), self.max_power)

        self.set_cells(value=norm)
        return 

    def bilinear_interpolation(self, pos):
        """
        Interpolazione bilineare del campo 2D 'field' alla posizione continua (x, y).
        Ritorna un valore float compreso tra 0 e 1.
        """
        x = pos[1]
        y = pos[0]
        if x > self.width - 1:
            x -= 1
        if y > self.height - 1:
            y -= 1

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
        return power
    
    def update(self):
        # Crea una perturbazione casuale
        perturbation = np.random.randn(self.width, self.height) * 0.15   
        # Applica la perturbazione alla distribuzione attuale
        power_distribution = self.data + gaussian_filter(perturbation, sigma=self.sigma)
        # Ritaglia ai limiti di [0, self.max_power] per evitare overflow
        norm = np.dot(np.divide(power_distribution - np.min(power_distribution), np.max(power_distribution) - np.min(power_distribution)), self.max_power)

    
        self.set_cells(value=norm)
        return
    
    def test_plot(self):
        plt.imshow(self.data, cmap='viridis')
        plt.colorbar()
        plt.show()
        return
    
    def plot(self, ax):
        ax.imshow(self.data, cmap='viridis')
        ax.colorbar()