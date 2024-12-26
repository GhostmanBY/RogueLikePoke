import os
import sys
from collections import OrderedDict
import requests
from tqdm import tqdm

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ruta_raiz)

from DB.DB_PokeAPI import DB_PokeAPI

class Peticones_Poke_API(DB_PokeAPI):
    def __init__(self):
            self.URL_pokemon = "https://pokeapi.co/api/v2/pokemon/?offset=0&limit="
            self.URL_Move_State = "https://pokeapi.co/api/v2/move/?offset=0&limit="
            self.Disc_traduccion_movimientos = {}
            self.GenI_moves = self.conseguir_disc_espesifico("https://pokeapi.co/api/v2/generation/1", "moves") 
            self.GenII_moves = self.conseguir_disc_espesifico("https://pokeapi.co/api/v2/generation/2", "moves") 
            self.GenIII_moves = self.conseguir_disc_espesifico("https://pokeapi.co/api/v2/generation/3", "moves") 
            self.all_moves = {move['name'] for move in (self.GenI_moves + self.GenII_moves + self.GenIII_moves)}
            self.stats_text = ["HP", "ATK", "DEF", "SATK", "SDEF", "VEL"]
            self.Stat_base = {}

    def Conseguir_Datos_Staticos_Pokemons(self):
        url = "https://pokeapi.co/api/v2/pokemon"
        respuesta_Main = requests.get(url)
        respuesta_Main.encoding = 'utf-8'
        
        if respuesta_Main.status_code == 200:
            data_Main = respuesta_Main.json()
            pbar = tqdm(range(151), desc="Cargando Pokémon")
            for i in pbar:
                respuesta_StatsBase = requests.get(data_Main['results'][i]['url'])
                respuesta_StatsBase.encoding = 'utf-8'

                if respuesta_StatsBase.status_code == 200:
                    data_StatBase = respuesta_StatsBase.json()
                    for j in range(len(data_StatBase['stats'])):
                        self.Stat_base.update({self.stats_text[j]:data_StatBase['stats'][j]['base_stat']})
                    self.Stat_base.update({"XP":data_StatBase['base_experience']})
                
                    self.Introduccir_Stat_base(data_StatBase['name'], self.Stat_base)
                    Name_pokemon = data_StatBase['name']
                    Elemento = self.traduccion(data_StatBase['types'][0]['type']['url'])
                    
                    habilidades_probable = []
                    for C_abilidad in data_StatBase['abilities']:
                        habilidad_traducida = self.traduccion(C_abilidad['ability']['url'])
                        habilidades_probable.append(habilidad_traducida)

                    Moves_posibles = {}
                    for movimiento in data_StatBase['moves']:
                        for version in movimiento['version_group_details']:
                            if version['version_group']['name'] == "firered-leafgreen":
                                movimiento_traducido = self.traduccion(movimiento['move']['url'])
                                Moves_posibles.update({movimiento_traducido: version['level_learned_at']})
                    
                    Moves_posibles_ordenados = OrderedDict(sorted(Moves_posibles.items(), key=lambda x: x[1]))
                    self.Introduccir_pokemon(Name_pokemon, Elemento, habilidades_probable, Moves_posibles_ordenados)
                    pbar.set_description(f"Procesando: {Name_pokemon}")

    def Conseguir_precicion_potencia_full(self):
        url = "https://pokeapi.co/api/v2/move"
        tmp_moves = []
        respuesta_Main = requests.get(url)
        respuesta_Main.encoding = 'utf-8'

        if respuesta_Main.status_code == 200:
            data_main = respuesta_Main.json()
            pbar = tqdm(range(len(data_main['results'])), desc="Cargando movimientos")
            for i in pbar:
                respuesta_values_move = requests.get(data_main['results'][i]['url'])
                respuesta_values_move.encoding = 'utf-8'
                if respuesta_values_move.status_code == 200:
                    data_Values = respuesta_values_move.json()
                    if data_main['results'][i]['name'] in self.all_moves:
                        name = self.traduccion(data_main['results'][i]['url'])
                        tipo = self.traduccion(data_Values['type']['url'])
                        Daño = self.traduccion(data_Values['damage_class']['url'])
                        efecto = {self.traduccion(data_Values['meta']['ailment']['url']): data_Values['meta']['ailment_chance']}
                        move_stat = {"Nombre":name, "Tipo":tipo, "Efecto": efecto, "Tipo_Daño": Daño,"Precicion":data_Values['accuracy'], "Potencia":data_Values['power'], "PP":data_Values['pp']}
                        tmp_moves.append(data_main['results'][i]['name'])
                        self.Introduccir_Moves(move_stat)
                        pbar.set_description(f"Procesando: {name}")
                    if len(tmp_moves) == len(self.all_moves):
                        return

    def Conseguir_naturalesas(self):
        url = "https://pokeapi.co/api/v2/nature/"
        respues_naturaleza = requests.get(url)
        respues_naturaleza.encoding = 'utf-8'

        if respues_naturaleza.status_code == 200:
            data_naturalezas = respues_naturaleza.json()
            pbar = tqdm(range(len(data_naturalezas['results'])), desc="Cargando naturalezas")
            for i in pbar:
                respuesta_natu_espesifica = requests.get(data_naturalezas['results'][i]['url'])
                respuesta_natu_espesifica.encoding = 'utf-8'
                if respuesta_natu_espesifica.status_code == 200:
                    data_especifica = respuesta_natu_espesifica.json()
                    Nombre = self.traduccion(data_naturalezas['results'][i]['url'])
                    Debuff = data_especifica['decreased_stat']['name'] if data_especifica['decreased_stat'] else None
                    Buff = data_especifica['increased_stat']['name'] if data_especifica['increased_stat'] else None
                    self.Introduccir_Naturalezas(Nombre, Debuff, Buff)
                    pbar.set_description(f"Procesando: {Nombre}")

    def traduccion(self, URL):
        respues_traduccion = requests.get(URL)
        respues_traduccion.encoding = 'utf-8'

        if respues_traduccion.status_code == 200:
            data_traduccion = respues_traduccion.json()
            for i in range(len(data_traduccion['names'])):
                if data_traduccion["names"][i]["language"]["name"] == "es":
                    name = data_traduccion["names"][i]["name"]
                    return name
    
    def conseguir_disc_espesifico(self, URL, name_disc):
        respuesta_disc = requests.get(URL)
        respuesta_disc.encoding = 'utf-8'

        if respuesta_disc.status_code == 200:
            data_disc = respuesta_disc.json()
            return data_disc[f'{name_disc}']

if __name__ == "__main__":
    peticion = Peticones_Poke_API()
    peticion.Crear_Tablas()
    peticion.Conseguir_Datos_Staticos_Pokemons()