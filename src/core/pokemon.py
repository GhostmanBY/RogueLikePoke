import os
import sys
import random
import json

# Configuración de la ruta del proyecto
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ruta_raiz)

from DB.DB_PokeAPI import DB_PokeAPI

class Pokemon(DB_PokeAPI):
    def __init__(self, pokemon, lvl, bot):
        # Initialize DB_PokeAPI without arguments
        super().__init__()
        # Initialize Pokemon-specific attributes
        self.pokemon = pokemon
        self.lvl = lvl
        self.bot = bot
        if bot == True:
            self.stat_pokemon = self.Stat_pokemon(pokemon)
        else:
            self.stat_pokemon = self.Stat_pokemon_player(pokemon, lvl)

    def numramdom(self, motivo, content=None, rango=0):
        if motivo == "naturalezas":
            if rango <= 0:
                raise ValueError("El rango debe ser mayor a 0 para 'naturalezas'.")
            return random.randint(1, rango)
        
        elif motivo == "Habilidad":
            if not isinstance(content, dict):
                raise TypeError("El parámetro 'content' debe ser un diccionario para 'Habilidad'.")
            
            habilidades = []
            peso = []

            for habilidad, valor in content.items():
                habilidades.append(habilidad)
                peso.append(1 if valor else 2)  # Peso menor si es True, mayor si es False

            if not habilidades:
                raise ValueError("El parámetro 'content' no contiene habilidades.")
            
            # Selección aleatoria con ponderación
            return random.choices(habilidades, peso, k=1)[0]
        
        else:
            raise ValueError(f"Motivo '{motivo}' no es válido.")



    def Stat_pokemon(self, pokemon):
        datos_base = self.data_pokemon(pokemon)
        stat_base = self.data_pokemon(pokemon)
        naturalezas = self.data_natulazesa(self.numramdom("naturalezas", rango=25))
        print(json.loads(datos_base[3]))
        disc_pokemon = {
            "Nombre": datos_base[1],
            "Tipo": datos_base[2],
            "Habilidad": datos_base[3][self.numramdom("Habilidad", json.loads(datos_base[3]))],
            "Naturalezas": naturalezas[1],
            "HP": stat_base[2],
            "ATK": stat_base[3],
            "DEF": stat_base[4],
            "SATK": stat_base[5],
            "SDEF": stat_base[6],
            "SPEED": stat_base[7],
            "XP": stat_base[8],
        }
        # Aplicar modificadores de estadísticas basados en la naturaleza
        disc_pokemon[naturalezas[2]] *= 1.1 if naturalezas[2] != None else 1 
        disc_pokemon[naturalezas[3]] *= 1.1 if naturalezas[3] != None else 1
        return disc_pokemon

    def Stat_pokemon_player(self, pokemon, nombre_player):
        if os.path.exists(f"data_file_{nombre_player}.json"):
            with open(f"data_file_{nombre_player}.json", "r", encoding="utf-8") as file:
                data = json.loads(file)
            for i in range(len(data)):
                if data[i]["Pokemons"]["nombre"] == pokemon:
                    disc_pokemon = {
                        "Tipo": data[i]["Pokemons"]["tipo"],
                        "Habilidad": data[i]["Pokemons"]["habilidad"],
                        "Naturalezas": data[i]["Pokemons"]["naturaleza"],
                        "HP": data[i]["Pokemons"]["Stats"]["HP"],
                        "ATK": data[i]["Pokemons"]["Stats"]["ATK"],
                        "DEF": data[i]["Pokemons"]["Stas"]["DEF"],
                        "SATK": data[i]["Pokemons"]["Stats"]["SATK"],
                        "SDEF": data[i]["Pokemons"]["Stats"]["SDEF"],
                        "SPEED": data[i]["Pokemons"]["Stats"]["SPEED"],
                        "XP": data[i]["Pokemons"]["Stats"]["XP"],
                    }
                return disc_pokemon

    def atacar(self, movimiento):
        # Calculate base power
        power = movimiento.get('power', 0)
        if not power:
            return 0

        # Get attack and defense stats
        if movimiento.get('category') == 'physical':
            atk = self.stat_pokemon['ATK']
            defense = self.stat_pokemon['DEF']
        else:
            atk = self.stat_pokemon['SATK'] 
            defense = self.stat_pokemon['SDEF']

        # Calculate damage with basic formula
        damage = ((2 * 50 / 5 + 2) * power * (atk / defense)) / 50 + 2

        # Apply random factor (85-100%)
        damage *= random.uniform(0.85, 1.0)

        # Apply STAB bonus if move type matches pokemon type
        if movimiento.get('type') in self.stat_pokemon['Tipo']:
            damage *= 1.5

        return int(damage)
    
if __name__ == "__main__":
    pk = Pokemon("bulbasaur", 5, True)
    print(pk.stat_pokemon)