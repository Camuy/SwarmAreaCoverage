import os
import sys

sys.path.insert(0, os.path.abspath("../../../.."))

from model import WECswarm
from mesa.visualization import Slider, SolaraViz, make_space_component

# Pre-compute markers for different angles (e.g., every 10 degrees)


def wec_draw(agent):
    neighbors = len(agent.neighbors)

    # Calculate the angle
    deg = agent.angle
    # Round to nearest 10 degrees
    rounded_deg = round(deg / 10) * 10 % 360

    # using cached markers to speed things up
    if neighbors <= 1:
        return {"color": "red", "size": 20}
    elif neighbors >= 2:
        return {"color": "green", "size": 20}


model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "population_size": Slider(
        label="Number of WECs",
        value=100,
        min=10,
        max=1000,
        step=10,
    ),
    "width": 100,
    "height": 100,
    "speed": Slider(
        label="Max speed of WEC",
        value=5,
        min=1,
        max=20,
        step=1,
    ),
    "vision": Slider(
        label="Vision (radius)",
        value=10,
        min=1,
        max=50,
        step=1,
    ),
    "separation": Slider(
        label="Minimum Separation",
        value=2,
        min=1,
        max=5000,
        step=1,
    ),
}

model = WECswarm()

page = SolaraViz(
    model,
    components=[make_space_component(agent_portrayal=wec_draw, backend="matplotlib")],
    model_params=model_params,
    name="WEC Swarm Model",
)
page  # noqa