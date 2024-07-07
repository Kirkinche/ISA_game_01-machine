# src/character.py

import random
from RPG_character_utils import RPGCharacter
from items import get_item_by_name

class Character(RPGCharacter):
    def __init__(self, race, name, gender, job, world_size):
        super().__init__(race, name, gender, job)
        self.position = (random.randint(0, world_size - 1), random.randint(0, world_size - 1))  # Random starting position
        self.max_health = self.life
        self.current_health = self.max_health  # Start with full health
        self.inventory = [{"name": "Sword", "type": "weapon", "bonus": 5, "price": 10}]  # Starting with a sword

    def restore_health(self):
        self.current_health = self.max_health
        print(f"{self.name}'s health is fully restored to {self.current_health}")

    def buy_item(self, item_name):
        item = get_item_by_name(item_name)
        if item and self.money >= item["price"]:
            self.inventory.append(item)
            self.money -= item["price"]
            print(f"{self.name} bought {item['name']} for {item['price']} gold.")
        else:
            print(f"{self.name} does not have enough gold to buy {item_name}.")

    def sell_item(self, item_name):
        for item in self.inventory:
            if item["name"] == item_name:
                self.inventory.remove(item)
                self.money += item["price"]
                print(f"{self.name} sold {item_name} for {item['price']} gold.")
                return
        print(f"{item_name} not found in inventory.")

    def get_weapon_bonus(self):
        return sum(item["bonus"] for item in self.inventory if item["type"] == "weapon")

    def get_armor_bonus(self):
        return sum(item["bonus"] for item in self.inventory if item["type"] == "armor")

def create_character(name, world_size, race="Human", gender="Male", job="Warrior"):
    return Character(race, name, gender, job, world_size)
