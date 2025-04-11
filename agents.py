"""A Boid (bird-oid) agent for implementing Craig Reynolds's Boids flocking model.

This implementation uses numpy arrays to represent vectors for efficient computation
of flocking behavior.
"""

import numpy as np

from mesa.experimental.continuous_space import ContinuousSpaceAgent

class WEC(ContinuousSpaceAgent):
    """A Boid-style flocker agent.

    The agent follows three behaviors to flock:
        - Cohesion: steering towards neighboring agents
        - Separation: avoiding getting too close to any other agent
        - Alignment: trying to fly in the same direction as neighbors

    Boids have a vision that defines the radius in which they look for their
    neighbors to flock with. Their speed (a scalar) and direction (a vector)
    define their movement. Separation is their desired minimum distance from
    any other Boid.
    """

    def __init__(
        self,
        model,
        space,
        position=(0, 0),
        max_speed=1,
        speed = 0,
        direction=(1, 1),
        vision=1,
        separation=1,
        cohere=0.03,
        separate=0.015,
        match=0.05,
        power: float = 0,
        battery: int = 50,
        consume: int = 1,
        efficiency: float = 0.3,
        WEC_power = 0
        ):
        """Create a new Boid flocker agent.

        Args:
            model: Model instance the agent belongs to
            speed: Distance to move per step
            direction: numpy vector for the Boid's direction of movement
            vision: Radius to look around for nearby Boids
            separation: Minimum distance to maintain from other Boids
            cohere: Relative importance of matching neighbors' positions (default: 0.03)
            separate: Relative importance of avoiding close neighbors (default: 0.015)
            match: Relative importance of matching neighbors' directions (default: 0.05)
        """
        super().__init__(space, model)
        self.position = position
        self.max_speed = max_speed
        self.speed = speed
        self.direction = direction
        self.vision = vision ## radius of comunication
        self.separation = separation
        self.neighbors = []
        self.angle = 0.0  # represents the angle at which the boid is moving
        self.power = self.model.power.get_power(self.position)
        self.battery = battery
        self.consume = consume ## rate of usage of the battery to move
        self.efficiency = efficiency
        self.WEC_power = WEC_power

    def update_status(self):
        self.neighbors, _ = self.get_neighbors_in_radius(radius=self.vision)
        self.get_speed()
        self.model.power.get_power(self.position)
        self.get_battery()

    def step(self):
        # get updates
        self.update_status()
        
        self.neighbors = [n for n in self.neighbors if n is not self]
        
        
        # If no neighbors, maintain current direction
        if not self.neighbors:
            self.move()
            return
        
        # self.neighbors = [n for n in self.neighbors if n.power > self.power] # filtered neigbors visible only if they have major pawer then me
        
        self.get_direction()
        
        # Move boid
        self.move()
    
    def get_direction(self):
        targets = self.get_target() # highest power function, i go where the power is higher
        
        delta = self.space.calculate_difference_vector(self.position, agents=targets)
        delta = delta[0] + self.agoraphobic()
        #cohere_vector = delta.sum(axis=0) * self.cohere_factor
        #separation_vector = (-1 * delta[distances < self.separation].sum(axis=0) * self.separate_factor)
        #match_vector = (np.asarray([n.direction for n in neighbors]).sum(axis=0) * self.match_factor)

        # Normalize direction vector
        norm = np.linalg.norm(delta)

        if norm > self.separation:
            self.direction = np.divide(delta, norm)
        if norm < self.separation:
            self.agoraphobic()
        if targets[0] == self:
            self.direction = [0, 0]
            
        
        print("direction =", self.direction)
        return
    
    def get_target(self):
        target = self.neighbors[0]
        for n in self.neighbors:
            if self.model.power.get_power(n.position) > self.model.power.get_power(target.position):
                target = n
        return [target]
    
    def agoraphobic(self):
        crawd = []
        for n in self.neighbors:
            distance = self.space.calculate_distances(point=self.position, agents=[n])
            if distance[0] < self.separation:
                crawd.append(n)
        delta = self.space.calculate_difference_vector(self.position, agents=crawd)
        delta = delta[0]
        norm = np.linalg.norm(delta)
        self.direction = -np.divide(delta, norm)
        return self.direction
    
    def get_recharge(self):
        return np.multiply(self.efficiency, self.model.power.get_power(self.position))
    
    def get_speed(self):
        self.speed = np.multiply(np.divide(self.battery, 100), self.max_speed) # linear function, can be sigmoid or others
        return
    
    def get_consume(self):
        return (self.speed ** 3) * self.consume
    
    def get_battery(self):
        self.WEC_power = self.get_recharge() - self.get_consume()
        self.battery += self.get_recharge() - self.get_consume()
        if self.battery > 100:
            self.battery = 100
        return

    def move(self):
        position = self.position + self.direction * self.speed
        if position[0] < self.space.x_min:
            self.direction[0] = -self.direction[0]
            position[0] = self.position[0] + self.direction[0] * self.speed
        if position[0] > self.space.x_max:
            self.direction[0] = -self.direction[0]
            position[0] = self.position[0] + self.direction[0] * self.speed
        if position[1] < self.space.y_min:
            self.direction[1] = -self.direction[1]
            position[1] = self.position[1] + self.direction[1] * self.speed
        if position[1] > self.space.y_max:
            self.direction[1] = -self.direction[1]
            position[1] = self.position[1] + self.direction[1] * self.speed
        self.position = position
        return