"""
Lógica del jugador y sus estadísticas
"""

class Player:
    def __init__(self, name):
        self.name = name
        self.pokemon = []
        self.items = []

    def add_pokemon(self, pokemon):
        """Añade un pokemon al equipo"""
        try:
            self.pokemon.append(pokemon)
            return True
        except:
            print("No se pudo añadir el pokemon")
            return False
