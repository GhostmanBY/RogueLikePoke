"""
Clase para manejar los niveles y arcos
"""
import random
from .event import Event

class Level:
    def __init__(self, level_data):
        self.id = level_data["id"]
        self.name = level_data["name"]
        self.difficulty = level_data["difficulty"]
        self.pokemon_min_level = level_data["pokemon_min_level"]
        self.pokemon_max_level = level_data["pokemon_max_level"]
        self.available_pokemon = level_data["available_pokemon"]
        self.events = []
    
    def add_event(self, event):
        """Añade un evento al nivel"""
        self.events.append(event)
    
    def generate_events(self, player, max_events=1):
        """Genera eventos aleatorios para el nivel"""
        events = []
        for _ in range(random.randint(0, max_events)):
            event = self.generate_random_event()
            events.append(event)
            if event.effect:
                player.apply_effect(event.effect)
        return events
    
    def generate_random_event(self):
        """Genera un evento aleatorio basado en las probabilidades"""
        # Implementar lógica de generación de eventos
        pass
