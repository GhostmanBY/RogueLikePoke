import os
import sys 
from collections import OrderedDict
import requests

# Configura la ruta del proyecto para importar módulos locales
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ruta_raiz)

# Importa la clase base que maneja la base de datos
from DB.DB_PokeAPI import DB_PokeAPI

class Peticones_Poke_API(DB_PokeAPI):
    """
    Clase para gestionar peticiones a la PokeAPI y almacenar datos en la base de datos.
    Hereda de DB_PokeAPI para las operaciones de base de datos.
    """
    def __init__(self):
        super().__init__()  # Llama al constructor de la clase base
        # Diccionarios de los pokemons de la primera generacion hasta la tercera
        self.GenI_pokemons = self.conseguir_disc_espesifico("https://pokeapi.co/api/v2/generation/1", "pokemon_species")
        self.all_pokemon = {pokemon_species['name'] for pokemon_species in self.GenI_pokemons}
        # Diccionarios de los movimietos de la primera generacion hasta la tercera
        self.GenI_moves = self.conseguir_disc_espesifico("https://pokeapi.co/api/v2/generation/1", "moves") 
        self.GenII_moves = self.conseguir_disc_espesifico("https://pokeapi.co/api/v2/generation/2", "moves") 
        self.GenIII_moves = self.conseguir_disc_espesifico("https://pokeapi.co/api/v2/generation/3", "moves") 
        #Movimientos unicos de Pokémon Colosseum y XD
        shadow_moves = {
            "shadow-rush", "shadow-blast", "shadow-blitz", "shadow-bolt", "shadow-break",
            "shadow-chill", "shadow-end", "shadow-fire", "shadow-rave", "shadow-storm",
            "shadow-wave", "shadow-down", "shadow-half", "shadow-hold", "shadow-mist",
            "shadow-panic", "shadow-shed", "shadow-sky"
        }
        # Se usa un conjunto para agrupar solo los nombres
        self.all_moves = {move['name'] for move in (self.GenI_moves + self.GenII_moves + self.GenIII_moves) if move['name'] not in shadow_moves}
        # Simples listas para iterar las stat
        self.stats_text = ["HP", "ATK", "DEF", "SATK", "SDEF", "VEL"]
        # Diccionario para almacenar temporalmente las estadísticas base de cada Pokémon
        self.Stat_base = {}
        # Lista auxiliar naturalezas
        self.lista_naturalezas = {"attack": "ATK", "defense": "DEF", "special-attack": "SATK", "special-defense": "SDEF", "speed": "SPEED"}
    def Conseguir_Datos_Staticos_Pokemons(self):
        """
        Obtiene y almacena los datos completos de los primeros 151 Pokémon.
        Incluye:
        - Estadísticas base
        - Tipo elemental
        - Habilidades posibles
        - Movimientos aprendibles en FireRed/LeafGreen
        """
        url = "https://pokeapi.co/api/v2/pokemon" # url inicial
        tmp_pokemon = []
        while url:
            try:
                respuesta_Main = requests.get(url) # Consulta Principal
                respuesta_Main.encoding = 'utf-8'
                respuesta_Main.raise_for_status()
            except requests.RequestException as e:
                print(f"Error al obtener datos de {url}: {e}")
                break

            if respuesta_Main.status_code == 200:
                data_Main = respuesta_Main.json() 
                # Barra de carga de consola
                for i in range(len(data_Main['results'])):
                    try:
                        respuesta_StatsBase = requests.get(data_Main['results'][i]['url']) # Consulta de cada Pokemon
                        respuesta_StatsBase.encoding = 'utf-8'
                        respuesta_StatsBase.raise_for_status()
                    except requests.RequestException as e:
                        print(f"Error al obtener datos de {data_Main['results'][i]['url']}: {e}")
                        continue

                    if respuesta_StatsBase.status_code == 200:
                        data_StatBase = respuesta_StatsBase.json() 
                        # Procesa y almacena las estadísticas base
                        for j in range(len(data_StatBase['stats'])):
                            self.Stat_base.update({self.stats_text[j]:data_StatBase['stats'][j]['base_stat']})
                        self.Stat_base.update({"XP":data_StatBase['base_experience']})
                    
                        # Funcion de la DB para ingresar las estadisticas de cada Pokemon
                        self.Introduccir_Stat_base(data_StatBase['name'], self.Stat_base)

                        Name_pokemon = data_StatBase['name'] # Nombre de los pokemon
                        Elemento = self.traduccion(data_StatBase['types'][0]['type']['url']) # El tipo de cada pokemon y traduce el mismo al español
                        
                        # Captura las posibles habilidades de cada pokemon, traducidas al español y las agrega a una lista
                        habilidades_probable = {}
                        for C_abilidad in data_StatBase['abilities']:
                            habilidad_traducida = self.traduccion(C_abilidad['ability']['url'])
                            habilidades_probable.update({habilidad_traducida:C_abilidad['is_hidden']})
                        # Captura los movimientos que puede aprender cada pokemon, los traduce al español y las agrega a un disccionario con el nivel que lo aprende
                        Moves_posibles = {}
                        for movimiento in data_StatBase['moves']:
                            for version in movimiento['version_group_details']:
                                if version['version_group']['name'] == "firered-leafgreen":
                                    movimiento_traducido = self.traduccion(movimiento['move']['url'])
                                    Moves_posibles.update({movimiento_traducido: version['level_learned_at']})
                        
                        # Ordena los movimientos por nivel de aprendizaje
                        Moves_posibles_ordenados = OrderedDict(sorted(Moves_posibles.items(), key=lambda x: x[1])) # Ordena de menor a mayor con respecto del nivel 
                        # Funcion de la DB que ingresa los datos de cada pokemon
                        self.Introduccir_pokemon(Name_pokemon, Elemento, habilidades_probable, Moves_posibles_ordenados)
                        tmp_pokemon.append(Name_pokemon)
                        if len(tmp_pokemon) == len(self.all_pokemon):
                            return
                    elif respuesta_StatsBase.status_code == 404:
                        print(f"Error 404: {data_Main['results'][i]['url']} no encontrado")
                    
            url = data_Main.get('next') # se usa la url que proporciona la API para ir cambiando de pagina, cada 20 elementos
            
    def Conseguir_Stat_Movimientos(self):
        """
        Recopila y almacena información detallada sobre los movimientos Pokémon.
        Procesa solo los movimientos de las generaciones I, II y III.
        Incluye:
        - Tipo de movimiento
        - Categoría de daño
        - Efectos secundarios y probabilidades
        - Estadísticas (precisión, potencia, PP)
        """
        url = "https://pokeapi.co/api/v2/move/" # url inicial
        tmp_moves = [] # Lista para limitar la cantidad de movimientos ya que solo se quieren los de la tercera generacion
        while url:
            try:
                respuesta_Main = requests.get(url) # Consulta principal
                respuesta_Main.encoding = 'utf-8'
                respuesta_Main.raise_for_status()
            except requests.RequestException as e:
                print(f"Error al obtener datos de {url}: {e}")
                break

            if respuesta_Main.status_code == 200:
                data_main = respuesta_Main.json()
                # Barra de cargar
                for i in range(len(data_main['results'])):
                    try:
                        respuesta_values_move = requests.get(data_main['results'][i]['url']) # Consulta de cada movimiento
                        respuesta_values_move.encoding = 'utf-8'
                        respuesta_values_move.raise_for_status()
                    except requests.RequestException as e:
                        print(f"Error al obtener datos de {data_main['results'][i]['url']}: {e}")
                        continue

                    if respuesta_values_move.status_code == 200:
                        data_Values = respuesta_values_move.json()
                        # Evalua si esta dentro del conjunto de movimientos de las generaciones 1, 2 y 3
                        if data_main['results'][i]['name'] in self.all_moves: 
                            name = self.traduccion(data_main['results'][i]['url']) # Nombre del movimiento, traducido
                            tipo = self.traduccion(data_Values['type']['url']) # Tipo del movmiento, traducido
                            Daño = self.traduccion(data_Values['damage_class']['url']) # Tipo de daño del movmiento, traducido
                            efecto = {self.traduccion(data_Values['meta']['ailment']['url']): data_Values['meta']['ailment_chance']} # Efecto del movmiento, traducido y en un diccionario con su chance de afectar
                            move_stat = {"Nombre":name, "Tipo":tipo, "Efecto": efecto, "Tipo_Daño": Daño,"Precicion":data_Values['accuracy'], "Potencia":data_Values['power'], "PP":data_Values['pp']} # Diccionario final de todos los datos juntos
                            tmp_moves.append(data_main['results'][i]['name']) # Agrega a la lista temporal para que se puedan ir contando
                            self.Introduccir_Moves(move_stat) # Funcion de la DB para ingresar los datos de cada movimiento
                            # Cuando sea igual la cantidad de movimientos de la lista tmp_moves al conjunto all_move, se corta la iteracion con un total de 354 movimientos
                            if len(tmp_moves) == len(self.all_moves): 
                                return
            url = data_main.get('next')
    
    def Conseguir_naturalesas(self):
        """
        Obtiene y almacena todas las naturalezas Pokémon disponibles.
        Cada naturaleza puede afectar positivamente una estadística (Buff)
        y negativamente otra (Debuff).
        """
        url = "https://pokeapi.co/api/v2/nature/"
        # Procesa cada naturaleza y sus efectos
        while url:
            try:
                respues_naturaleza = requests.get(url)
                respues_naturaleza.encoding = 'utf-8'
                respues_naturaleza.raise_for_status()
            except requests.RequestException as e:
                print(f"Error al obtener datos de {url}: {e}")
                break

            if respues_naturaleza.status_code == 200:
                data_naturalezas = respues_naturaleza.json()
                # Muestra progreso con barra de carga
                for i in range(len(data_naturalezas['results'])):
                    try:
                        respuesta_natu_espesifica = requests.get(data_naturalezas['results'][i]['url'])
                        respuesta_natu_espesifica.encoding = 'utf-8'
                        respuesta_natu_espesifica.raise_for_status()
                    except requests.RequestException as e:
                        print(f"Error al obtener datos de {data_naturalezas['results'][i]['url']}: {e}")
                        continue

                    if respuesta_natu_espesifica.status_code == 200:
                        data_especifica = respuesta_natu_espesifica.json()
                        # Traduce y almacena la información de cada naturaleza
                        Nombre = self.traduccion(data_naturalezas['results'][i]['url'])
                        # Maneja casos donde la naturaleza no afecta estadísticas
                        Debuff = data_especifica['decreased_stat']['name'] if data_especifica['decreased_stat'] else None
                        Debuff = self.lista_naturalezas[Debuff] if Debuff else None
                        Buff = data_especifica['increased_stat']['name'] if data_especifica['increased_stat'] else None
                        Buff = self.lista_naturalezas[Buff] if Buff else None

                        self.Introduccir_Naturalezas(Nombre, Debuff, Buff)
            url = data_naturalezas.get('next')

    def traduccion(self, URL):
        """
        Función auxiliar para traducir textos de la API al español.
        Args:
            URL (str): URL del recurso a traducir
        Returns:
            str: Texto traducido al español, o None si no se encuentra traducción
        """
        try:
            respues_traduccion = requests.get(URL)
            respues_traduccion.encoding = 'utf-8'
            respues_traduccion.raise_for_status()
        except requests.RequestException as e:
            print(f"Error al obtener datos de {URL}: {e}")
            return None

        if respues_traduccion.status_code == 200:
            data_traduccion = respues_traduccion.json()
            for i in range(len(data_traduccion['names'])):
                if data_traduccion["names"][i]["language"]["name"] == "es":
                    name = data_traduccion["names"][i]["name"]
                    return name
                elif data_traduccion["names"][i]["language"]["name"] == "en":
                    name = data_traduccion["names"][i]["name"]
                    return name
    
    def conseguir_disc_espesifico(self, URL, name_disc):
        """
        Obtiene un diccionario específico de la API.
        Args:
            URL (str): URL base del recurso
            name_disc (str): Nombre del diccionario a extraer
        Returns:
            dict: Diccionario con la información solicitada, o None si hay error
        """
        try:
            respuesta_disc = requests.get(URL)
            respuesta_disc.encoding = 'utf-8'
            respuesta_disc.raise_for_status()
        except requests.RequestException as e:
            print(f"Error al obtener datos de {URL}: {e}")
            return None

        if respuesta_disc.status_code == 200:
            data_disc = respuesta_disc.json()
            return data_disc.get(name_disc)

# Punto de entrada del script
if __name__ == "__main__":
    peticion = Peticones_Poke_API()
    peticion.Crear_Tablas()
    peticion.Conseguir_Datos_Staticos_Pokemons()
    peticion.Conseguir_Stat_Movimientos()
    peticion.Conseguir_naturalesas()