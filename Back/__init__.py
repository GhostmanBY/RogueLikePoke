import requests
import json

respuesta = requests.get("https://pokeapi.co/api/v2/pokemon/4/")

data = respuesta.json()
Abilidad_probable = []
for C_abilidad in data['abilities']:
    Abilidad_probable.append(C_abilidad['ability']['name'])
print(Abilidad_probable)