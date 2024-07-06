# src/character.py

import random
from RPG_character_utils import RPGCharacter

class Character(RPGCharacter):
    def __init__(self, race, name, gender, job, world_size):
        super().__init__(race, name, gender, job)
        self.position = (random.randint(0, world_size - 1), random.randint(0, world_size - 1))  # Random starting position
        self.max_health = self.life
        self.current_health = self.max_health  # Start with full health

    def restore_health(self):
        self.current_health = self.max_health
        print(f"{self.name}'s health is fully restored to {self.current_health}")

def create_character(name, world_size, race="Human", gender="Male", job="Warrior"):
    return Character(race, name, gender, job, world_size)
