# src/character.py

import random
from RPG_character_utils import RPGCharacter
from items import get_item_by_name
from skills import skills

class Character(RPGCharacter):
    def __init__(self, race, name, gender, job, world_size):
        super().__init__(race, name, gender, job)
        self.position = (random.randint(0, world_size - 1), random.randint(0, world_size - 1))  # Random starting position
        self.max_health = self.life
        self.current_health = self.max_health  # Start with full health
        self.inventory = [{"name": "Sword", "type": "weapon", "bonus": 5, "price": 10}]  # Starting with a sword
        self.skills = {}  # Initialize empty skills dictionary
        self.current_health = self.max_health  # Start with full health
       

    def __repr__(self):
        return f"{self.name}: {self.current_health}/{self.max_health} HP, {self.money} gold"

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

    def collect_treasure(self, treasure):
        if treasure["type"] == "gold":
            self.money += treasure["amount"]
            print(f"{self.name} found {treasure['amount']} gold coins!")
        elif treasure["type"] == "item":
            self.inventory.append({"name": treasure["name"], "type": "treasure", "value": treasure["value"]})
            print(f"{self.name} found a {treasure['name']} worth {treasure['value']} gold!")
        elif treasure["type"] == "consumable":
            self.inventory.append({"name": treasure["name"], "type": "consumable", "effect": treasure["effect"], "value": treasure["value"]})
            print(f"{self.name} found a {treasure['name']}!")

    def learn_skill(self, skill_name):
        for skill_category in skills.values():
            if skill_name in skill_category:
                self.skills[skill_name] = skill_category[skill_name]
                print(f"{self.name} learned the skill {skill_name}!")
                return
        print(f"Skill {skill_name} does not exist.")

    def use_skill(self, skill_name):
        if skill_name in self.skills:
            skill = self.skills[skill_name]
            attribute = skill["attribute"]
            if isinstance(attribute, list):
                effect = skill["effect"](*[getattr(self, attr) for attr in attribute])
            else:
                effect = skill["effect"](getattr(self, attribute))
            print(f"{self.name} uses {skill_name}! {skill['description']} Effect: {effect}")
            return effect
        else:
            print(f"{self.name} does not know the skill {skill_name}!")

    def serialize_skills(self):
        # Convert skills to a serializable format
        return {skill_name: {"description": skill["description"], "attribute": skill["attribute"]} for skill_name, skill in self.skills.items()}

    def deserialize_skills(self, serialized_skills):
        # Reconstruct skills from the serialized format
        for skill_name, skill_data in serialized_skills.items():
            for skill_category in skills.values():
                if skill_name in skill_category:
                    self.skills[skill_name] = skill_category[skill_name]
                    break
    
    def is_defeated(self):
        return self.current_health <= 0

    @classmethod
    def from_save(cls, save_data):
        character = cls(save_data["race"], save_data["name"], save_data["gender"], save_data["job"], world_size=10)
        character.position = tuple(save_data["position"])
        character.current_health = save_data["current_health"]
        character.max_health = save_data["max_health"]
        character.money = save_data["money"]
        character.inventory = save_data["inventory"]
        character.deserialize_skills(save_data.get("skills", {}))
        return character

def create_character(name, world_size, race="Human", gender="Male", job="Warrior"):
    return Character(race, name, gender, job, world_size)
