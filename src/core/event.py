"""
Generación y manejo de eventos aleatorios
"""

class Event:
    def __init__(self, event_type, description, probability, effect=None):
        self.event_type = event_type
        self.description = description
        self.probability = probability
        self.effect = effect
    
    def apply_effect(self, player):
        """Aplica el efecto del evento al jugador si existe"""
        if self.effect:
            self.effect(player)
    
    def get_dialog(self):
        """Retorna la descripción del evento para mostrar como diálogo"""
        return self.description
