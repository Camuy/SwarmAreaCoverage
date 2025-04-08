from mesa import Agent

class EnergyAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.energy = 0

    def step(self):
        # Spostamento casuale
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        # Raccolta energia dalla cella
        x, y = self.pos
        energy_here = self.model.energy_grid[y][x]
        self.energy += energy_here
        self.model.energy_grid[y][x] = 0  # energia consumata