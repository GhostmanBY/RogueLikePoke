"""
Lógica del jugador y sus estadísticas
"""

class Player:
    def __init__(self, name):
        self.name = name
        self.pokemon = []
        self.items = []
        self.position = (0, 0)
        
    def move(self, dx, dy):
        """Mueve al jugador en el mapa"""
        self.position = (self.position[0] + dx, self.position[1] + dy)
        
    def add_pokemon(self, pokemon):
        """Añade un pokemon al equipo"""
        if len(self.pokemon) < 6:
            self.pokemon.append(pokemon)
            return True
        return False
