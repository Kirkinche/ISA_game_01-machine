# src/combat.py

import random
from RPG_character_utils import RPGCharacter

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def attack(self, attacker, defender):
        damage = max(1, attacker.strength - defender.constitution // 2)  # Simple damage formula
        defender.current_health -= damage
        print(f"{attacker.name} attacks {defender.name} for {damage} damage!")

    def start_battle(self):
        print(f"A wild {self.enemy.name} appears!")
        while self.player.current_health > 0 and self.enemy.current_health > 0:
            self.attack(self.player, self.enemy)
            if self.enemy.current_health <= 0:
                print(f"{self.enemy.name} is defeated!")
                break
            self.attack(self.enemy, self.player)
            if self.player.current_health <= 0:
                print("You have been defeated!")
                break

def create_enemy():
    names = ["Goblin", "Orc", "Troll", "Bandit", "Skeleton"]
    name = random.choice(names)
    enemy = RPGCharacter(race="Goblin", name=name, gender="Male", job="Warrior")
    enemy.current_health = enemy.max_health  # Ensure enemy has current_health attribute
    return enemy
