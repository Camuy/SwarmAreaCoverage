import solara
from  mesa_viz_tornado.ModularVisualization import ModularServer 
from mesa_viz_tornado.modules import CanvasGrid, ChartModule

from model import EnergyModel  # <-- lo creiamo dopo
from agents import EnergyAgent  # <-- lo creiamo dopo

# Funzione per disegnare gli agenti sulla griglia
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "r": 0.5,
        "Color": "red",
        "Layer": 0,
    }
    return portrayal

# Visualizzazione
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# Modulo per i grafici (esempio, modificabile)
chart = ChartModule([{"Label": "count", "Color": "black"}])

# Server
server = ModularServer(
    EnergyModel,
    [grid, chart],
    "Area Coverage",
    {"width": 10, "height": 10},
)
#
# App Solara
@solara.component
def Page():
    solara.Title("Mesa + Solara Demo")
    solara.Markdown("## Simulation Interface")
    solara.Button("Start simulation", on_click=lambda: server.launch())
