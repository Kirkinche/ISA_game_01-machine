# src/save_load.py

import json
import os

SAVE_FILE = "game_save.json"

def save_game(player, world):
    game_state = {
        "player": {
            "name": player.name,
            "race": player.race,
            "gender": player.gender,
            "job": player.job,
            "position": player.position,
            "current_health": player.current_health,
            "max_health": player.max_health,
            "money": player.money,
            "inventory": player.inventory,
            "skills": player.serialize_skills()  # Save serialized skills
        },
        "world": {
            "size": world.size,
            "map": world.map.map
        }
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(game_state, file)
    print("Game saved successfully.")

def load_game():
    if not os.path.exists(SAVE_FILE):
        print("No saved game found.")
        return None, None

    with open(SAVE_FILE, "r") as file:
        game_state = json.load(file)

    return game_state
