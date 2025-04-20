# model.py - Simulador de una planta del Hospital Ruber Juan Bravo

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from agents import BaseAgente, Paciente, Medico, Enfermero, PersonalLimpieza, Recepcionista, Zona
import random
from mesa.datacollection import DataCollector


# model_hospital.py

class HospitalModel(Model):
    def __init__(self, width=6, height=6, num_pacientes=5, num_medicos=2, num_enfermeros=2, num_limpieza=1, num_recepcionistas=1):
        self.grid = MultiGrid(width, height, torus=False)
        self.random = random.Random()
        self.schedule = SimultaneousActivation(self)
        self.current_hour = 8
        self.pacientes_atendidos = 0

        # Referencias a zonas específicas del hospital (puedes cambiarlas si tus coords cambian)
        self.entrada = (0, 3)
        self.recepcion = (1, 3)
        self.espera = (2, 2)
        self.urgencias = (4, 1)
        self.sala_tecnica = (2, 0)
        self.salida= (0,3)

        # Definición de zonas en la planta
        self.zonas = {
            (0, 3): {"id": "E1", "tipo": "entrada"},
            (1, 3): {"id": "R1", "tipo": "recepcion"},
            (2, 3): {"id": "P1", "tipo": "pasillo"},
            (3, 3): {"id": "C1", "tipo": "consulta"},
            (4, 3): {"id": "C2", "tipo": "consulta"},
            (2, 2): {"id": "S1", "tipo": "espera"},
            (3, 2): {"id": "C3", "tipo": "consulta"},
            (4, 2): {"id": "C4", "tipo": "consulta"},
            (2, 1): {"id": "P2", "tipo": "pasillo"},
            (3, 1): {"id": "WC1", "tipo": "baño"},
            (4, 1): {"id": "U1", "tipo": "urgencias"},
            (2, 0): {"id": "L1", "tipo": "tecnico"},
        }

        self.posiciones_libres = list(self.zonas.keys())

        # Crear agentes
        self.crear_agentes(Paciente, num_pacientes)
        self.crear_agentes(Medico, num_medicos)
        self.crear_agentes(Enfermero, num_enfermeros)
        self.crear_agentes(PersonalLimpieza, num_limpieza)
        self.crear_agentes(Recepcionista, num_recepcionistas)

        # Zonas fijas visuales
        self.grid.place_agent(Zona("entrada", self, "Entrada"), self.entrada)
        self.grid.place_agent(Zona("recepcion", self, "Recepción"), self.recepcion)
        self.grid.place_agent(Zona("espera", self, "Espera"), self.espera)
        self.grid.place_agent(Zona("urgencias", self, "Urgencias"), self.urgencias)
        self.grid.place_agent(Zona("limpieza", self, "Limpieza"), self.sala_tecnica)


    

        print("AGENTES CREADOS:")
        for agent in self.schedule.agents:
            print(agent.unique_id, agent.pos)

        # Recogida de datos
        self.datacollector = DataCollector(
            model_reporters={
                "PacientesAtendidos": get_pacientes_atendidos,
                "MedicosActivos": get_medicos_activos,
                "ZonasOcupadas": get_zonas_ocupadas,
            }
        )
    def crear_agentes(self, clase_agente, cantidad):
        for i in range(cantidad):
            pos = self.random.choice(self.posiciones_libres)
            nombre = clase_agente.__name__.replace("Personal", "")  # más limpio
            agente = clase_agente(f"{nombre}_{i}", self, pos)
            self.grid.place_agent(agente, pos)
            self.schedule.add(agente)
    def step(self):
        self.schedule.step()
        self.current_hour += 1
        if self.current_hour > 21:
            self.current_hour = 8
        
        self.datacollector.collect(self)



    
#Para recogida de datos

def get_pacientes_atendidos(model):
    return model.pacientes_atendidos

def get_medicos_activos(model):
    return sum(1 for a in model.schedule.agents if isinstance(a, Medico))

def get_zonas_ocupadas(model):
    posiciones_ocupadas = [agent.pos for agent in model.schedule.agents]
    zonas_definidas = model.zonas.keys()
    return sum(1 for z in zonas_definidas if z in posiciones_ocupadas)


