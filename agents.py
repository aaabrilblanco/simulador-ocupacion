# agents.py

from mesa import Agent
import random


class BaseAgente(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.next_pos = None  # ← NUEVO: para guardar la posición futura

    def step(self):
        self.decidir_destino()

    def advance(self):
        if self.next_pos is not None:
            self.model.grid.move_agent(self, self.next_pos)
            self.pos = self.next_pos
            self.next_pos = None

    def decidir_destino(self):
        pass  # ← Las subclases lo implementarán

    def movimiento_hacia(self, destino):
        x, y = self.pos
        dx = 1 if destino[0] > x else -1 if destino[0] < x else 0
        dy = 1 if destino[1] > y else -1 if destino[1] < y else 0
        return (x + dx, y + dy)

class Paciente(BaseAgente):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)
        self.estado = "entrada"

    def decidir_destino(self):
        if self.estado == "entrada":
            destino = self.model.espera
            if self.pos == destino:
                self.estado = "espera"
            else:
                self.next_pos = self.movimiento_hacia(destino)
        elif self.estado == "espera":
            # Selecciona una consulta disponible
            consultas = [pos for pos, data in self.model.zonas.items() if data["tipo"] == "consulta"]
            if consultas:
                destino = random.choice(consultas)
                if self.pos == destino:
                    self.estado = "consulta"
                else:
                    self.next_pos = self.movimiento_hacia(destino)
        elif self.estado == "consulta":
            destino = self.model.entrada
            if self.pos == destino:
                self.estado = "salida"
                self.model.pacientes_atendidos += 1
            else:
                self.next_pos = self.movimiento_hacia(destino)


class Medico(BaseAgente):
    def decidir_destino(self):
        consultas = [pos for pos, data in self.model.zonas.items() if data["tipo"] == "consulta"]
        if consultas:
            destino = random.choice(consultas)
            self.next_pos = self.movimiento_hacia(destino)


class Enfermero(BaseAgente):
    def decidir_destino(self):
        vecinos = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        libres = [pos for pos in vecinos if self.model.grid.is_cell_empty(pos)]
        if libres:
            self.next_pos = random.choice(libres)


class PersonalLimpieza(BaseAgente):
    def decidir_destino(self):
        if self.model.current_hour in range(16, 21):
            destino = random.choice(list(self.model.zonas.keys()))
        else:
            destino = self.model.sala_tecnica
        self.next_pos = self.movimiento_hacia(destino)




class Recepcionista(BaseAgente):
    def decidir_destino(self):
        self.next_pos = self.model.recepcion  # siempre vuelve a su puesto



class Zona(Agent):
    def __init__(self, unique_id, model, tipo):
        super().__init__(unique_id, model)
        self.tipo = tipo


