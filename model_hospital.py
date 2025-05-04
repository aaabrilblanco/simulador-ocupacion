import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import PacienteAgent, MedicoAgent


class LineaSeparacion(Agent):
    def __init__(self, unique_id, model, planta):
        super().__init__(unique_id, model)
        self.planta = planta
    
    def render(self):
        return {
            "Shape": "rect",
            "w": 10,  # Ancho completo del grid
            "h": 1,
            "Filled": "true",
            "Color": "black",
            "Layer": 0
        }

class CeldaHospital(Agent):
    def __init__(self, unique_id, model, tipo, planta):
        super().__init__(unique_id, model)
        self.tipo = tipo
        self.planta = planta
        self.color_map = {
            "administracion": "pink",
            "consultas": "orange",
            "b.quirúrjico": "yellow",
            "hospitalizacion": "lightgreen",
            "h.de_dia": "lightblue",
            "lab": "gray",
            "uci": "red",
            "esterilizacion": "purple",
            "ascensor": "black",
            "admision": "cyan",
            "cafeteria": "brown",
            "b.obstetrico": "magenta",
            "sign": "white",
            "archivo": "beige",
            "rehabilitacion": "teal",
            "dialisis": "navy",
            "radiologia": "blue",
            "urgencias": "darkred",
            "extracciones": "lightyellow",
            "formacion": "lavender"
        }
    
    def render(self):
        return {
            "Shape": "rect",
            "w": 1,
            "h": 1,
            "Filled": "true",
            "Color": self.color_map.get(self.tipo, "white"),
            "Layer": self.planta,
            "text": self.tipo[:3],
            "text_color": "black"
        }

class HospitalModel(Model):
    def __init__(self, width=10, height=24):
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.ocupadas = set()

        
        self.habitaciones = {
            2: [
                ("administracion", [(0, 21),(1, 21),(2, 21),
                                    (0, 22),(2, 22),(0, 22)]),
                ("formacion",[(4, 18),(4, 19)]),
                ("hospitalizacion", [(5, 20),(6, 20),(7, 20)]),
                ("h.de_dia", [(5, 19),(6, 19)]),
                ("lab", [(7, 19)]),
                ("uci", [(5, 18)]),
                ("esterilizacion", [(6, 18),(7, 18)]),
                ("ascensor", [(8, 19)])
            ],
            1: [
                ("b.quirúrjico", [(4, 9),(5, 9),(6, 9),(7, 9),(8, 9)]),
                ("b.obstetrico", [(5, 10), (6, 10), (7, 10), (8, 10)]),
                ("admision", [(1, 14)]),
                ("cafeteria", [(2, 14),(3, 14),(4, 14)]),
                ("hospitalizacion", [(5,12), (6, 12), (7, 12), (8, 12)]),
                ("consultas", [(0, 10), (1, 10), (2, 10), (3, 10),
                               (0, 11),(1, 11),(2, 11),(3, 11),
                               (0, 12),(1, 12),(2, 12),(3, 12)]),
                ("ascensor", [(8, 10)])
            ],
            0: [
                ("urgencias",[(4,0),(5,0),(6,0),(7,0),(8,0)]),
                ("archivo", [(2,5),(3,5)]), 
                ("rehabilitacion", [(0, 3),(1, 3)]),
                ("hospitalizacion", [(4, 5), (5, 5), (6, 5), (7, 5)]), #arriba
                ("hospitalizacion", [(4, 3), (5, 3), (6, 3), (7, 3)]), #abajo
                ("dialisis", [(0, 1), (1, 1)]),
                ("extracciones", [(2,1)]),
                ("radiologia", [(4,1),(5,1),(6,1),(7,1)]),
                ("ascensor", [(8, 1)])
            ]
        }
        
        # Crear habitaciones
        agent_id = 0
        for planta, habitaciones in self.habitaciones.items():
            for tipo, coords in habitaciones:
                for coord in coords:
                    agente = CeldaHospital(agent_id, self, tipo, planta)
                    self.grid.place_agent(agente, coord)
                    self.schedule.add(agente)
                    agent_id += 1
        
        # Crear líneas separadoras
        self.crear_linea(0, 7, 9, 7)  # Entre planta 0 y 1
        self.crear_linea(0, 16, 9, 16)  # Entre planta 1 y 2


        # Agente paciente
        paciente = PacienteAgent(unique_id=agent_id, model=self, planta=0, destino=(5, 5))  # ejemplo de destino
        self.grid.place_agent(paciente, (1, 1))  # posición inicial
        self.schedule.add(paciente)
        self.ocupadas.add(((1, 1), 0))  # marca la celda como ocupada
        agent_id += 1


        # Agente médico
        medico = MedicoAgent(unique_id=agent_id, model=self, planta=0)
        self.grid.place_agent(medico, (3, 3))  # posición inicial
        self.schedule.add(medico)
        self.ocupadas.add(((3, 3), 0))  # marca la celda como ocupada
        agent_id += 1

    
    def crear_linea(self, x_start, y, x_end, y_end):
        """Crea una línea horizontal de agentes"""
        for x in range(x_start, x_end + 1):
            agente = LineaSeparacion(f"linea_{x}_{y}", self, 0)
            self.grid.place_agent(agente, (x, y))
    
    def es_celda_valida(self, pos, planta):
        return (pos, planta) in self.ocupadas or any(
            agent for agent in self.grid.get_cell_list_contents(pos)
            if isinstance(agent, CeldaHospital) and agent.planta == planta
        )

    def step(self):
        self.schedule.step()