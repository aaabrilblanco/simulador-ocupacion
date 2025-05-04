from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from model_hospital import HospitalModel, CeldaHospital, LineaSeparacion
from agents import PacienteAgent, MedicoAgent

def agent_portrayal(agent):
    return agent.render()

grid = CanvasGrid(agent_portrayal, 10, 24, 500, 800)

server = ModularServer(
    HospitalModel,
    [grid],
    "Simulación de Hospital con Agentes",
    {"width": 10, "height": 30}
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()
