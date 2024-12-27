"""
Utilidades para interactuar con la PokeAPI y gestionar datos de Pokémon
"""
import os
import sys 
import requests
from tqdm import tqdm

class PokeAPI:
    """
    Clase para gestionar peticiones a la PokeAPI y almacenar datos de Pokémon.
    """
    def __init__(self):
        self.GenI_pokemons = self.get_generation_data("https://pokeapi.co/api/v2/generation/1", "pokemon_species")
        self.all_pokemon = {pokemon_species['name'] for pokemon_species in self.GenI_pokemons}
        self.GenI_moves = self.get_generation_data("https://pokeapi.co/api/v2/generation/1", "moves")
        self.stats_text = ["HP", "ATK", "DEF", "SATK", "SDEF", "VEL"]
        self.base_stats = {}

    def get_generation_data(self, url, data_type):
        """Obtiene datos específicos de una generación"""
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get(data_type, [])
        return []

    def get_pokemon_data(self):
        """
        Obtiene datos de los primeros 151 Pokémon.
        Incluye estadísticas base, tipo, habilidades y movimientos.
        """
        url = "https://pokeapi.co/api/v2/pokemon"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for pokemon in tqdm(data['results'][:151], desc="Cargando Pokémon"):
                pokemon_data = requests.get(pokemon['url']).json()
                stats = {
                    stat['stat']['name']: stat['base_stat'] 
                    for stat in pokemon_data['stats']
                }
                yield {
                    'name': pokemon_data['name'],
                    'stats': stats,
                    'types': [t['type']['name'] for t in pokemon_data['types']],
                    'abilities': [a['ability']['name'] for a in pokemon_data['abilities']]
                }
