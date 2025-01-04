import random
from ..core.pokemon import Pokemon
class Level():
    def __init__(self, stage, level_number):
        Soleado = Event("Soleado", "Hoy es un día soleado, te sientes con más energía", 0.5)
        Lluvioso = Event("Lluvioso", "Hoy es un día lluvioso, te sientes más cansado", 0.5)
        Tormena_arena = Event("Tormena de arena", "Hoy es un día de tormenta de arena, te sientes más cansado", 0.5)
        Nieve = Event("Nieve", "Hoy es un día de nieve, te sientes más cansado", 0.5)
        if stage == 1:
            self.enemies = ["pikachu", "charmander", "squirtle", "bulbasaur", "pidgey", "rattata", "spearow", "ekans", "sandshrew", "nidoran"]
        elif stage == 2:
            self.enemies = ["clefairy", "vulpix", "jigglypuff", "zubat", "oddish", "paras", "venonat", "diglett", "meowth", "psyduck"]
        elif stage == 3:
            self.enemies = ["mankey", "growlithe", "poliwag", "abra", "machop", "bellsprout", "tentacool", "geodude", "ponyta", "slowpoke"]
        elif stage == 4:
            self.enemies = ["magnemite", "farfetch'd", "doduo", "seel", "grimer", "shellder", "gastly", "onix", "drowzee", "krabby"]
        elif stage == 5:
            self.enemies = ["voltorb", "exeggcute", "cubone", "hitmonlee", "hitmonchan", "lickitung", "koffing", "rhyhorn", "chansey", "tangela"]
        elif stage == 6:
            self.enemies = ["kangaskhan", "horsea", "goldeen", "staryu", "scyther", "pinsir", "tauros", "magikarp", "lapras", "ditto"]
        elif stage == 7:
            self.enemies = ["eevee", "porygon", "omanyte", "kabuto", "aerodactyl", "snorlax", "articuno", "zapdos", "moltres", "dratini"]
        elif stage == 8:
            self.enemies = ["dragonair", "dragonite", "mewtwo", "mew", "raichu", "arcanine", "alakazam", "machamp", "golem", "gengar"]
        self.stage = stage
        self.level = level_number
        self.events = [Soleado,Lluvioso,Tormena_arena,Nieve]

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
    
    def generate_enemie(self, min = 5, max = 8):
        enemigos = []
        for i in range(random.randint(min,max)):
            enemigo = Pokemon(random.choice(self.enemies))
            enemigos.append(enemigo)
        random.shuffle(self.enemies)
        return enemigos
    def dialog(self, event):
        # Retorna la descripción del evento para mostrar como diálogo
        return event.description

class Event:
    def __init__(self, event_type, description, probability):
        self.probability = probability
        self.event_type = event_type
        self.description = description