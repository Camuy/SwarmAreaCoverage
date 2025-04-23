import os
import sys
import solara
import solara.lab                           # NEW ─ tabs live here
sys.path.insert(0, os.path.abspath("../../../.."))

from model import WECswarm,WECSTATIC
from mesa.visualization import Slider, SolaraViz, make_space_component, draw_space, make_plot_component
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
    if neighbors > 1:
        if agent.battery > 20:
            if agent.battery > 90:
                return {"color": "blue", "size": 20}
            if agent.WEC_power >= 0:
                return {"color": "green", "size": 20}
            else:
                return {"color": "yellow", "size": 20}
        elif agent.battery < 20:
            if agent.battery < 10:
                return {"color": "black", "size": 20}
            return {"color": "grey", "size": 20}
        
    

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": {
        "type": "InputText",
        "value": 100,
        "label": "width",
    },
    "height": {
        "type": "InputText",
        "value": 100,
        "label": "height",
    },
    "population_size": Slider(
        label="Number of WECs",
        value=100,
        min=1,
        max=100,
        step=1,
    ),
    "speed": Slider(
        label="Max speed of WEC",
        value=0.5,
        min=0,
        max=1,
        step=0.01,
    ),
    "vision": Slider(
        label="Vision (radius)",
        value=20,
        min=1,
        max=100,
        step=1,
    ),
    "separation": Slider(
        label="Minimum Separation",
        value=9,
        min=1,
        max=30,
        step=1,
    ),
    "efficiency": Slider(
        label="Conversion efficiency",
        value=0.70,
        min=0,
        max=1,
        step=0.01,
    ),
    "consume": Slider(
        label="Consume of energy to move",
        value=1,
        min=0,
        max=2,
        step=0.01,
    ),
    "load": Slider(
        label="Amount of work",
        value=1,
        min=0,
        max=2,
        step=0.01,
    ),
    "battery": Slider(
        label="Starting amount of energy",
        value=30,
        min=0,
        max=100,
        step=1,
    ),
}


# reuse your component lists
comps_dynamic = [
    make_space_component(agent_portrayal=wec_draw, backend="matplotlib"),
    make_plot_component(measure="avg_battery"),
    make_plot_component(measure="connections"),
    make_plot_component(measure="total_load"),
]

comps_static = [
    make_space_component(agent_portrayal=wec_draw, backend="matplotlib"),
    make_plot_component(measure="avg_battery"),
    make_plot_component(measure="total_load"),
]

# ─── two little wrapper components ────────────────────────────────────────
@solara.component
def DynamicPage():
    #model = solara.reactive(WECswarm())         #if we want to simulation doesn't intrupt when we switch to the other page
    model = WECswarm()
    return SolaraViz(
        model,
        components = comps_dynamic,
        model_params=model_params,
        name="Dynamic WECs",
    )

@solara.component
def StaticPage():
    #model = solara.reactive(WECSTATIC())                 #if we want to simulation doesn't intrupt when we switch to the other page
    model = WECSTATIC()
    return SolaraViz(
        model,
        components = comps_static,
        model_params=model_params,
        name="Static WECs",
    )

# ─── tell Solara about our two routes ────────────────────────────────────
routes = [
    solara.Route(path="",       component=DynamicPage, label="Dynamic"),
    solara.Route(path="static", component=StaticPage,  label="Static"),
]
