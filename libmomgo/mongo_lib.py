import os
import logging
from pymongo import MongoClient

logging.basicConfig(level=logging.INFO)

CLIENT = MongoClient(os.environ["DB_PORT_27017_TCP_ADDR"], 27017)
DB = CLIENT.pokedex

def insert(value):
    DB.pokedex.insert_one(value)

    
def find_one(region, number, evo_method: bool = True):
    pokemon = DB.pokedex.find_one({"number": number, "region": region})
    logging.warn(pokemon)
    if evo_method is True:
        if pokemon["evolution"] is True and pokemon.get("evolutions"):
            evolutions = list()
            for evolution in pokemon["evolutions"]:
                pokemon_evolution = DB.pokedex.find_one({"_id": evolution})
                evolutions.append(pokemon_evolution)
            pokemon["evolutions"] = evolutions

    return pokemon


def find_many(types: list):
    pokemons = DB.pokedex.find({"types": {"$in": types}})
    pokemon_list = list()
    for pokemon in pokemons:
        if pokemon["evolution"] is True and pokemon.get("evolutions"):
            evolutions = list()
            for evolution in pokemon["evolutions"]:
                pokemon_evolution = DB.pokedex.find_one({"_id": evolution})
                evolutions.append(pokemon_evolution)
            pokemon["evolutions"] = evolutions
            pokemon_list.append(pokemon)
        else:
            pokemon_list.append(pokemon)
        
    # pokemons = [pokemon for pokemon in pokemons]
    return pokemon_list


def update(region, number, evolutions: list):
    pokemon = find_one(region, number)
    evo_pokemon_ids = list()
    for evolution in evolutions:
        evo_pokemon = find_one(region, evolution["number"])
        evo_pokemon_ids.append(evo_pokemon["_id"])

    evolutions = {"$set": {"evolutions": evo_pokemon_ids}}
    try:
        DB.pokedex.update_one(pokemon, evolutions)
        pokemon = find_one(region, number, False)
        return pokemon
    except:
        raise Exception("Update fail")


def delete_one(region, number):
    delete_pokemon = find_one(region, number)
    pokemon_id = delete_pokemon["_id"]
    if delete_pokemon:
        DB.pokedex.delete_one(delete_pokemon)
        pokemons = DB.pokedex.find({"evolutions": {"$in": [pokemon_id]}})
        # not complete
        for pokemon in pokemons:
            pokemon["evolutions"].remove(pokemon_id)
            evolutions = {"$set": {"evolutions": pokemon["evolutions"]}}
            logging.warn(evolutions)
            del pokemon["evolutions"]
            DB.pokedex.update_one(pokemon, evolutions)
    else:
        # wish return 400
        raise Exception("Pokedex is null")
