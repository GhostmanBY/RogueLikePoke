"""
Lógica del combate por turnos
"""

class Combat:
    def __init__(self, player_pokemon, wild_pokemon):
        self.player_pokemon = player_pokemon
        self.wild_pokemon = wild_pokemon
        self.turn = 0
        
    def execute_turn(self, player_action):
        """Ejecuta un turno de combate"""
        pass
        
    def is_combat_over(self):
        """Verifica si el combate ha terminado"""
        return (self.player_pokemon.hp <= 0 or 
                self.wild_pokemon.hp <= 0)
