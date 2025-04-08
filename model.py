from mesa import Model
from mesa.space import MultiGrid
#from mesa.time import RandomActivation

from agents import EnergyAgent

class EnergyModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, torus=False)
        #self.schedule = RandomActivation(self)
        self.energy_grid = [[self.random.randint(0, 5) for _ in range(width)] for _ in range(height)]