import json
import os
import sys
import sqlite3

# Configuración de la ruta del proyecto
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(ruta_raiz)

class DB_PokeAPI():
    """Manejador de base de datos SQLite para almacenar información de Pokémon"""
    def __init__(self):
        pass
    
    def Connecion_DB(self):
        """Establece conexión con la base de datos
        Returns:
            sqlite3.Connection: Objeto de conexión a la DB
        """
        try:
            conn = sqlite3.connect("DB/DB_PokeAPI.db")
            return conn
        except sqlite3.Error as e:
            print(f"El error que ocurrio fue {e}")
            return None
    
    def Crear_Tablas(self):
        """Crea las tablas necesarias si no existen:
        - Pokemons: Información básica del Pokémon
        - StatsBase: Estadísticas base
        - Movimientos: Movimientos disponibles
        - Naturalezas: Modificadores de estadísticas
        """
        conn = self.Connecion_DB()
        c = conn.cursor()
        
        # Tabla para datos básicos del Pokémon
        c.execute(
            """CREATE TABLE IF NOT EXISTS Pokemons (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Tipo TEXT NOT NULL,
            Abilidad JSON NOT NULL,
            Movimientos JSON NOT NULL)"""
        )
        
        # Tabla para estadísticas base
        c.execute(
            """CREATE TABLE IF NOT EXISTS StatsBase (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            HP INTEGER,
            ATK INTEGER,
            DEF INTEGER,
            SATK INTEGER,
            SDEF INTEGER,
            SPEED INTEGER,
            XP INTEGER)"""
        )
        
        # Tabla para movimientos
        c.execute("""CREATE TABLE IF NOT EXISTS Movimientos(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Tipo TEXT NOT NULL,
            Tipo_Daño TEXT NOT NULL,
            Efecto JSON NOT NULL,
            PP INTEGER NOT NULL,
            Potencia INTEGER,
            Precicion INTEGER)""")
        
        # Tabla para naturalezas
        c.execute("""CREATE TABLE IF NOT EXISTS Naturalezas(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre TEXT NOT NULL,
            Debuff TEXT,
            Buff TEXT)""")
        
        conn.commit()
        conn.close()
    
    def Introduccir_pokemon(self, Pokemon, Tipo, Abilidad, Movimientos):
        """Inserta un nuevo Pokémon en la base de datos
        Args:
            Pokemon (str): Nombre del Pokémon
            Tipo (str): Tipo del Pokémon
            Abilidad (dict): Habilidades del Pokémon
            Movimientos (list): Lista de movimientos
        """
        conn = self.Connecion_DB()
        c = conn.cursor()
        
        instruccion = f"INSERT INTO Pokemons(Nombre, Tipo, Abilidad, Movimientos) VALUES(?,?,?,?)"
        c.execute(instruccion, (Pokemon, Tipo, json.dumps(Abilidad), json.dumps(Movimientos)))
        
        conn.commit()
        conn.close()
    
    def Introduccir_Stat_base(self, Pokemon_ID, Stat):
        """Inserta estadísticas base de un Pokémon
        Args:
            Pokemon_ID (str): Nombre del Pokémon
            Stat (dict): Diccionario con estadísticas base
        """
        conn = self.Connecion_DB()
        c = conn.cursor()
        
        instruccion = f"INSERT INTO StatsBase(Nombre, HP, ATK, DEF, SATK, SDEF, SPEED, XP) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(instruccion, (Pokemon_ID, Stat["HP"], Stat["ATK"], Stat["DEF"], Stat["SATK"], Stat["SDEF"], Stat["VEL"], Stat["XP"]))
        
        conn.commit()
        conn.close()
    
    def Introduccir_Moves(self, Moviemiento):
        """Inserta un nuevo movimiento en la base de datos
        Args:
            Moviemiento (dict): Diccionario con datos del movimiento
        """
        conn = self.Connecion_DB()
        c = conn.cursor()
        
        instruccion = f"INSERT INTO Movimientos(Nombre, Tipo, Tipo_Daño, Efecto, PP, Potencia, Precicion) VALUES (?, ?, ?, ?, ?, ?, ?)"
        c.execute(instruccion, (Moviemiento["Nombre"], Moviemiento["Tipo"], Moviemiento["Tipo_Daño"], 
                              json.dumps(Moviemiento["Efecto"]), Moviemiento["PP"], 
                              Moviemiento["Potencia"], Moviemiento["Precicion"]))
        
        conn.commit()
        conn.close()
    
    def Introduccir_Naturalezas(self, Nombre, Debuff, Buff):
        """Inserta una nueva naturaleza
        Args:
            Nombre (str): Nombre de la naturaleza
            Debuff (str): Estadística que disminuye
            Buff (str): Estadística que aumenta
        """
        conn = self.Connecion_DB()
        c = conn.cursor()
        
        instruccion = f"INSERT INTO Naturalezas(Nombre, Debuff, Buff) VALUES (?, ?, ?)"
        c.execute(instruccion, (Nombre, Debuff, Buff))
        
        conn.commit()
        conn.close()

if __name__ == "__main__":
    api = DB_PokeAPI()