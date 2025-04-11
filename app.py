import os
import sys
import solara

sys.path.insert(0, os.path.abspath("../../../.."))

from model import WECswarm
from mesa.visualization import Slider, SolaraViz, make_space_component, draw_space
from mesa.visualization.utils import update_counter
from matplotlib import pyplot as plt


# Pre-compute markers for different angles (e.g., every 10 degrees)
def make_space_component(
    agent_portrayal: None = None,
    propertylayer_portrayal: dict | None = None,
    post_process: None = None,
    backend: str = "matplotlib",
    **space_drawing_kwargs,
):
    
    if backend == "matplotlib":
        return make_mpl_space_component(
            agent_portrayal,
            propertylayer_portrayal,
            post_process,
            **space_drawing_kwargs,
        )
    else:
        raise ValueError(
            f"unknown backend {backend}, must be one of matplotlib, altair"
        )

def make_mpl_space_component(
    agent_portrayal: None = None,
    propertylayer_portrayal: dict | None = None,
    post_process: None = None,
    **space_drawing_kwargs,
):
    """Create a Matplotlib-based space visualization component.

    Args:
        agent_portrayal: Function to portray agents.
        propertylayer_portrayal: Dictionary of PropertyLayer portrayal specifications
        post_process : a callable that will be called with the Axes instance. Allows for fine tuning plots (e.g., control ticks)
        space_drawing_kwargs : additional keyword arguments to be passed on to the underlying space drawer function. See
                               the functions for drawing the various spaces for further details.

    ``agent_portrayal`` is called with an agent and should return a dict. Valid fields in this dict are "color",
    "size", "marker", "zorder", alpha, linewidths, and edgecolors. Other field are ignored and will result in a user warning.

    Returns:
        function: A function that creates a SpaceMatplotlib component
    """
    if agent_portrayal is None:

        def agent_portrayal(a):
            return {}

    def MakeSpaceMatplotlib(model):
        return SpaceMatplotlib(
            model,
            agent_portrayal,
            propertylayer_portrayal,
            post_process=post_process,
            **space_drawing_kwargs,
        )

    return MakeSpaceMatplotlib

@solara.component
def SpaceMatplotlib(
    model,
    agent_portrayal,
    propertylayer_portrayal,
    dependencies: list[any] | None = None,
    post_process: None = None,
    **space_drawing_kwargs,
):
    """Create a Matplotlib-based space visualization component."""
    update_counter.get()

    space = getattr(model, "grid", None)
    if space is None:
        space = getattr(model, "space", None)

    fig = plt.Figure()
    ax = fig.add_subplot()

    ax.imshow(
        X=model.power.data,
        cmap='inferno',
        alpha=1,
    )
    
    draw_space(
        space,
        agent_portrayal,
        propertylayer_portrayal=propertylayer_portrayal,
        ax=ax,
        **space_drawing_kwargs,
    )

    if post_process is not None:
        post_process(ax)

    solara.FigureMatplotlib(
        fig, format="png", bbox_inches="tight", dependencies=dependencies
    )



def wec_draw(agent):
    neighbors = len(agent.neighbors)

    # Calculate the angle
    deg = agent.angle
    # Round to nearest 10 degrees
    rounded_deg = round(deg / 10) * 10 % 360

    # using cached markers to speed things up
    if neighbors <= 1:
        return {"color": "red", "size": 20}
    elif agent.WEC_power >= 0:
        return {"color": "green", "size": 20}
    elif agent.WEC_power < 0:
        return {"color": "yellow", "size": 20}

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "population_size": Slider(
        label="Number of WECs",
        value=50,
        min=1,
        max=100,
        step=1,
    ),
    "width": 100,
    "height": 100,
    "speed": Slider(
        label="Max speed of WEC",
        value=5,
        min=1,
        max=10,
        step=1,
    ),
    "vision": Slider(
        label="Vision (radius)",
        value=30,
        min=1,
        max=100,
        step=1,
    ),
    "separation": Slider(
        label="Minimum Separation",
        value=20,
        min=1,
        max=100,
        step=1,
    ),
    "efficiency": Slider(
        label="Conversion efficiency",
        value=0.3,
        min=0,
        max=1,
        step=0.01,
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