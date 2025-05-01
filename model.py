"""
Boids Flocking Model
===================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""

import os
import sys

sys.path.insert(0, os.path.abspath("../../../.."))


import numpy as np
from numpy.random import default_rng

from mesa import Model, DataCollector
from agents import WEC, GP, STATIC
from mesa.experimental.continuous_space import ContinuousSpace

from environment import Ocean


class WECswarm(Model):
    """Flocker model class. Handles agent creation, placement and scheduling."""

    def __init__(
        self,
        population_size=100,
        width=100,
        height=100,
        speed=1,
        vision=10,
        separation=5,
        efficiency=0.3,
        consume=1,
        battery=50,
        load = 0,
        seed=10,
    ):
        """Create a new Boids Flocking model.

        Args:
            population_size: Number of Boids in the simulation (default: 100)
            width: Width of the space (default: 100)
            height: Height of the space (default: 100)
            speed: How fast the Boids move (default: 1)
            vision: How far each Boid can see (default: 10)
            separation: Minimum distance between Boids (default: 2)
            cohere: Weight of cohesion behavior (default: 0.03)
            separate: Weight of separation behavior (default: 0.015)
            match: Weight of alignment behavior (default: 0.05)
            seed: Random seed for reproducibility (default: None)
        """
        super().__init__(seed=seed)
        self.rng = default_rng(seed=seed)                #To make the initial positioning of the agents in the Static and Dynamic environment simillar we add this

        self.cumulative_load = 0.0

        # Set up the space
        self.space = ContinuousSpace(
            [[0, width], [0, height]],
            torus=False,
            random=self.random,
            n_agents=population_size,
        )

        self.power = Ocean(width=width, height=height, max_power = 1, seed=seed)
        self.power.modify_ocean()

        
        #{"connections": lambda m: sum(len(a.neighbors) for a in m.agents),}
        #print(self.datacollector.agent_reporters)
        #agent_reporters={"battery": lambda a: a.battery},

        # Create and place the Boid agents
        positions = self.rng.random(size=(population_size, 2)) * self.space.size
        directions = self.rng.uniform(-1, 1, size=(population_size, 2))
        WEC.create_agents(
            self,
            population_size,
            self.space,
            position=positions,
            max_speed=speed,
            speed = 0,
            direction=directions,
            separation=separation,
            vision=vision,
            consume=consume,
            efficiency=efficiency,
            battery=battery,
            load = load,
        )

        model_reporter = {
            "avg_battery": lambda m: np.mean([a.battery for a in m.agents]),
            "connections": lambda m: np.sum([len(a.neighbors) for a in m.agents]),
            "total_load": lambda m: np.multiply(np.divide(np.sum([a.load for a in m.agents]), population_size), 100),
            "cumulative_load": lambda m: m.cumulative_load 
        }

        agent_reporter = {
            "battery": lambda a: a.battery,
            "WEC_power": lambda a: a.WEC_power
        }


        self.datacollector = DataCollector(model_reporters=model_reporter, agent_reporters=agent_reporter)

        # For tracking statistics
        self.average_heading = None
        self.update_average_heading()
        #self.datacollector.collect(self)
        self.count = 0


    # vectorizing the calculation of angles for all agents
    def calculate_angles(self):
        d1 = np.array([agent.direction[0] for agent in self.agents])
        d2 = np.array([agent.direction[1] for agent in self.agents])
        self.agent_angles = np.degrees(np.arctan2(d1, d2))
        for agent, angle in zip(self.agents, self.agent_angles):
            agent.angle = angle

    def update_average_heading(self):
        """Calculate the average heading (direction) of all Boids."""
        if not self.agents:
            self.average_heading = 0
            return

        headings = np.array([agent.direction for agent in self.agents])
        mean_heading = np.mean(headings, axis=0)
        self.average_heading = np.arctan2(mean_heading[1], mean_heading[0])

    def step(self):
        """Run one step of the model.
        All agents are activated in random order using the AgentSet shuffle_do method.
        """
        self.agents.shuffle_do("step")
        self.cumulative_load += sum(a.load for a in self.agents)

        self.datacollector.collect(self)
        #self.count += 1
        #if self.count == 300:
        #    self.power.modify_ocean()
        #    self.count = 0
        self.power.update()



class WECSTATIC(Model):
    """Flocker model class. Handles agent creation, placement and scheduling."""

    def __init__(
        self,
        population_size=100,
        width=100,
        height=100,
        speed=1,
        vision=10,
        separation=5,
        efficiency=0.3,
        consume=1,
        battery=50,
        load = 0,
        seed=10,
    ):
        """Create a new Boids Flocking model.

        Args:
            population_size: Number of Boids in the simulation (default: 100)
            width: Width of the space (default: 100)
            height: Height of the space (default: 100)
            speed: How fast the Boids move (default: 1)
            vision: How far each Boid can see (default: 10)
            separation: Minimum distance between Boids (default: 2)
            cohere: Weight of cohesion behavior (default: 0.03)
            separate: Weight of separation behavior (default: 0.015)
            match: Weight of alignment behavior (default: 0.05)
            seed: Random seed for reproducibility (default: None)
        """
        super().__init__()
        self.rng = default_rng(seed)            #To make the initial positioning of the agents in the Static and Dynamic environment similar, we add this
        self.cumulative_load = 0.0
        
        # Set up the space
        self.space = ContinuousSpace(
            [[0, width], [0, height]],
            torus=False,
            random=self.random,
            n_agents=population_size,
        )

        self.power = Ocean(width=width, height=height, max_power = 1, seed=seed)
        self.power.modify_ocean()

        
        #{"connections": lambda m: sum(len(a.neighbors) for a in m.agents),}
        #print(self.datacollector.agent_reporters)
        #agent_reporters={"battery": lambda a: a.battery},

        # Create and place the Boid agents
        positions = self.rng.random(size=(population_size, 2)) * self.space.size
        STATIC.create_agents(
            self,
            population_size,
            self.space,
            position=positions,
            max_speed=speed,
            speed = 0,
            separation=separation,
            vision=vision,
            consume=consume,
            efficiency=efficiency,
            battery=battery,
            load = load,
        )

        model_reporter = {
            "avg_battery": lambda m: np.mean([a.battery for a in m.agents]),
            "connections": lambda m: np.sum([len(a.neighbors) for a in m.agents]),
            "total_load": lambda m: np.multiply(np.divide(np.sum([a.load for a in m.agents]), population_size), 100),
            "cumulative_load": lambda m: m.cumulative_load 
        }

        agent_reporter = {
            "battery": lambda a: a.battery,
            "WEC_power": lambda a: a.WEC_power
        }


        self.datacollector = DataCollector(model_reporters=model_reporter, agent_reporters=agent_reporter)



    def step(self):
        """Run one step of the model.
        All agents are activated in random order using the AgentSet shuffle_do method.
        """
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
        self.cumulative_load += sum(a.load for a in self.agents)
        #self.count += 1
        #if self.count == 300:
        #    self.power.modify_ocean()
        #    self.count = 0
        self.power.update()


class WECgp(Model):
    """Flocker model class. Handles agent creation, placement and scheduling."""

    def __init__(
        self,
        population_size=100,
        width=100,
        height=100,
        speed=1,
        vision=10,
        separation=5,
        efficiency=0.3,
        consume=1,
        battery=50,
        load = 0,
        seed=10,
    ):
        """Create a new Boids Flocking model.

        Args:
            population_size: Number of Boids in the simulation (default: 100)
            width: Width of the space (default: 100)
            height: Height of the space (default: 100)
            speed: How fast the Boids move (default: 1)
            vision: How far each Boid can see (default: 10)
            separation: Minimum distance between Boids (default: 2)
            cohere: Weight of cohesion behavior (default: 0.03)
            separate: Weight of separation behavior (default: 0.015)
            match: Weight of alignment behavior (default: 0.05)
            seed: Random seed for reproducibility (default: None)
        """
        super().__init__(seed=seed)
        self.rng = default_rng(seed=seed)                #To make the initial positioning of the agents in the Static and Dynamic environment simillar we add this

        self.cumulative_load = 0.0

        # Set up the space
        self.space = ContinuousSpace(
            [[0, width], [0, height]],
            torus=False,
            random=self.random,
            n_agents=population_size,
        )

        self.power = Ocean(width=width, height=height, max_power = 1, seed=seed)
        self.power.modify_ocean()

        
        #{"connections": lambda m: sum(len(a.neighbors) for a in m.agents),}
        #print(self.datacollector.agent_reporters)
        #agent_reporters={"battery": lambda a: a.battery},

        # Create and place the Boid agents
        positions = self.rng.random(size=(population_size, 2)) * self.space.size
        directions = self.rng.uniform(-1, 1, size=(population_size, 2))
        GP.create_agents(
            self,
            population_size,
            self.space,
            position=positions,
            max_speed=speed,
            speed = 0,
            direction=directions,
            separation=separation,
            vision=vision,
            consume=consume,
            efficiency=efficiency,
            battery=battery,
            load = load,
        )

        model_reporter = {
            "avg_battery": lambda m: np.mean([a.battery for a in m.agents]),
            "connections": lambda m: np.sum([len(a.neighbors) for a in m.agents]),
            "total_load": lambda m: np.multiply(np.divide(np.sum([a.load for a in m.agents]), population_size), 100),
            "cumulative_load": lambda m: m.cumulative_load 
        }

        agent_reporter = {
            "battery": lambda a: a.battery,
            "WEC_power": lambda a: a.WEC_power
        }


        self.datacollector = DataCollector(model_reporters=model_reporter, agent_reporters=agent_reporter)

        # For tracking statistics
        self.average_heading = None
        self.update_average_heading()
        #self.datacollector.collect(self)
        self.count = 0


    # vectorizing the calculation of angles for all agents
    def calculate_angles(self):
        d1 = np.array([agent.direction[0] for agent in self.agents])
        d2 = np.array([agent.direction[1] for agent in self.agents])
        self.agent_angles = np.degrees(np.arctan2(d1, d2))
        for agent, angle in zip(self.agents, self.agent_angles):
            agent.angle = angle

    def update_average_heading(self):
        """Calculate the average heading (direction) of all Boids."""
        if not self.agents:
            self.average_heading = 0
            return

        headings = np.array([agent.direction for agent in self.agents])
        mean_heading = np.mean(headings, axis=0)
        self.average_heading = np.arctan2(mean_heading[1], mean_heading[0])

    def step(self):
        """Run one step of the model.
        All agents are activated in random order using the AgentSet shuffle_do method.
        """
        self.agents.shuffle_do("step")
        self.cumulative_load += sum(a.load for a in self.agents)

        self.datacollector.collect(self)
        #self.count += 1
        #if self.count == 300:
        #    self.power.modify_ocean()
        #    self.count = 0
        self.power.update()
