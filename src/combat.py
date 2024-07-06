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

    def defend(self, defender):
        defense_boost = defender.constitution // 2
        defender.current_health += defense_boost
        print(f"{defender.name} defends and recovers {defense_boost} health!")

    def player_turn(self):
        while True:
            print("\nChoose an action:")
            print("1. Attack")
            print("2. Defend")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                self.attack(self.player, self.enemy)
                break
            elif choice == '2':
                self.defend(self.player)
                break
            else:
                print("Invalid choice. Please try again.")

    def enemy_turn(self):
        action = random.choice(["attack", "defend"])
        if action == "attack":
            self.attack(self.enemy, self.player)
        else:
            self.defend(self.enemy)

    def start_battle(self):
        print(f"A wild {self.enemy.name} appears!")
        while self.player.current_health > 0 and self.enemy.current_health > 0:
            self.player_turn()
            if self.enemy.current_health <= 0:
                print(f"{self.enemy.name} is defeated!")
                return True
            self.enemy_turn()
            if self.player.current_health <= 0:
                print("You have been defeated!")
                return False
        return False

def create_enemy():
    names = ["Goblin", "Orc", "Troll", "Bandit", "Skeleton"]
    name = random.choice(names)
    enemy = RPGCharacter(race="Goblin", name=name, gender="Male", job="Warrior")
    enemy.current_health = enemy.max_health  # Ensure enemy has current_health attribute
    return enemy
