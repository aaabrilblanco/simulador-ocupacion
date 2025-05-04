from mesa import Agent
import random

class PacienteAgent(Agent):
    def __init__(self, unique_id, model, planta, destino):
        super().__init__(unique_id, model)
        self.planta = planta
        self.destino = destino

    def step(self):
        possible_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
        )

        valid_moves = [
            pos for pos in possible_moves
            if self.model.es_celda_valida(pos, self.planta)
        ]

        if valid_moves:
            # Libera la celda anterior
            self.model.ocupadas.discard((self.pos, self.planta))

            new_position = random.choice(valid_moves)
            self.model.grid.move_agent(self, new_position)

            # Marca la nueva posición como ocupada
            self.model.ocupadas.add((new_position, self.planta))
    
    def render(self):
        return {
            "Shape": "circle",
            "Color": "green",
            "r": 0.5,
            "Layer": 3,
            "text": "P",
            "text_color": "white"
        }


class MedicoAgent(Agent):
    def __init__(self, unique_id, model, planta):
        super().__init__(unique_id, model)
        self.planta = planta

    def step(self):
        possible_moves = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False
        )

        valid_moves = [
            pos for pos in possible_moves
            if self.model.es_celda_valida(pos, self.planta)
        ]

        if valid_moves:
            self.model.ocupadas.discard((self.pos, self.planta))

            new_position = random.choice(valid_moves)
            self.model.grid.move_agent(self, new_position)

            self.model.ocupadas.add((new_position, self.planta))
    def render(self):
        return {
            "Shape": "circle",
            "Color": "blue",
            "r": 0.5,
            "Layer": 3,
            "text": "M",
            "text_color": "black"
        }