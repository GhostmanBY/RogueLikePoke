import random
class Level():
    def __init__(self, arco, level_number):
        self.arco = arco
        self.level = level_number
        self.events = []
    
    def add_event(self, event):
        self.events.append(event)
    
    def generate_event(self, player: object, event_cantity_max: int = 1):
        # Lista para almacenar los eventos generados
        events = []
        # Genera un número aleatorio de eventos entre 0 y event_cantity_max
        for _ in range(random.randint(0, event_cantity_max)):
            # Genera un evento aleatorio y lo añade a la lista
            event = self.generate_random_event()
            events.append(event)
        # Aplica los efectos de cada evento al jugador
        for event in events:
            if event.effect != None:
                player.effect = event.effect
        return events
    
    def dialog(self, event):
        # Retorna la descripción del evento para mostrar como diálogo
        return event.description

class Event:
    def __init__(self, event_type, description, probability):
        self.probability = probability
        self.event_type = event_type
        self.description = description

if __name__ == "__main__":
    level1 = generate_level(arc=1, level_number=1)
    for event in level1.events:
        print(f"{event.event_type}: {event.description}")
