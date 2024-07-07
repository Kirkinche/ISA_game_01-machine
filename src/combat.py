# src/combat.py

import random
from character import Character  # Correct import

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def display_health(self):
        print(f"\n{self.player.name}'s Health: {self.player.current_health}/{self.player.max_health}")
        print(f"{self.enemy.name}'s Health: {self.enemy.current_health}/{self.enemy.max_health}")

    def attack(self, attacker, defender):
        weapon_bonus = attacker.get_weapon_bonus() if hasattr(attacker, 'get_weapon_bonus') else 0
        armor_bonus = defender.get_armor_bonus() if hasattr(defender, 'get_armor_bonus') else 0
        damage = max(1, attacker.strength + weapon_bonus - defender.constitution // 2 - armor_bonus)
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
            print("3. Escape")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                self.attack(self.player, self.enemy)
                return "continue"
            elif choice == '2':
                self.defend(self.player)
                return "continue"
            elif choice == '3':
                self.escape()
                return "escape"
            else:
                print("Invalid choice. Please try again.")

    def enemy_turn(self):
        action = random.choice(["attack", "defend"])
        if action == "attack":
            self.attack(self.enemy, self.player)
        else:
            self.defend(self.enemy)

    def escape(self):
        penalty = 10
        self.player.current_health -= penalty
        print(f"{self.player.name} escapes the battle but loses {penalty} health!")

    def start_battle(self):
        print(f"A wild {self.enemy.name} appears!")
        while self.player.current_health > 0 and self.enemy.current_health > 0:
            self.display_health()
            result = self.player_turn()
            if result == "escape":
                return "escape"
            if self.enemy.current_health <= 0:
                print(f"{self.enemy.name} is defeated!")
                return "victory"
            self.display_health()
            self.enemy_turn()
            if self.player.current_health <= 0:
                print("You have been defeated!")
                return "defeat"
        return "defeat"

def create_enemy():
    names = ["Goblin", "Orc", "Troll", "Bandit", "Skeleton"]
    name = random.choice(names)
    enemy = Character(race="Goblin", name=name, gender="Male", job="Warrior", world_size=10)
    enemy.current_health = enemy.max_health  # Ensure enemy has current_health attribute
    return enemy
