# server.py

from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from model_hospital import HospitalModel
from agents import Paciente, Medico, Enfermero, PersonalLimpieza, Recepcionista, Zona

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 1,
        "r": 0.8,
        "text_color": "white"
    }

    if isinstance(agent, Paciente):
        portrayal["Color"] = "blue"
        portrayal["text"] = "P"
    elif isinstance(agent, Medico):
        portrayal["Color"] = "red"
        portrayal["text"] = "M"
    elif isinstance(agent, Enfermero):
        portrayal["Color"] = "orange"
        portrayal["text"] = "E"
    elif isinstance(agent, PersonalLimpieza):
        portrayal["Color"] = "green"
        portrayal["text"] = "L"
    elif isinstance(agent, Recepcionista):
        portrayal["Color"] = "purple"
        portrayal["text"] = "R"
    elif isinstance(agent, Zona):
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "white"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["text"] = agent.tipo[0]  # Solo primera letra
        portrayal["text_color"] = "black"

    return portrayal




# Grid y Chart
grid = CanvasGrid(agent_portrayal, 6, 6, 600, 600)

chart = ChartModule([
    {"Label": "PacientesAtendidos", "Color": "Red"},
    {"Label": "MedicosActivos", "Color": "Green"},
    {"Label": "ZonasOcupadas", "Color": "Blue"},
])

# Solo una instancia de server, con grid y chart
server = ModularServer(
    HospitalModel,
    [grid, chart],
    "Simulador Planta Hospital ",
    {
        "width": 6,
        "height": 6,
        "num_pacientes": 5,
        "num_medicos": 2,
        "num_enfermeros": 2,
        "num_limpieza": 1,
        "num_recepcionistas": 1
    }
)

server.port = 8521
server.launch()
