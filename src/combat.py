# src/combat.py

import random
from character import Character

class Combat:
    def __init__(self, player = Character(race=Any, name=Any, gender=Any, job=Any, world_size=Any), enemy = Character(race=Any, name=Any, gender=Any, job=Any, world_size=Any), display_callback):
        self.player = player
        self.enemy = enemy
        self.display_callback = display_callback  # Callback to display messages in the UI

    def display_health(self):
        health_info = f"\n{self.player.name}'s Health: {self.player.current_health}/{self.player.max_health}\n"
        health_info += f"{self.enemy.name}'s Health: {self.enemy.current_health}/{self.enemy.max_health}\n"
        self.display_callback(health_info)

    def attack(self, attacker = Character(race=Any, name=Any, gender=Any, job=Any, world_size=Any), defender= Character(race=Any, name=Any, gender=Any, job=Any, world_size=Any)):
        weapon_bonus = attacker.get_weapon_bonus() if hasattr(attacker, 'get_weapon_bonus') else 0
        armor_bonus = defender.get_armor_bonus() if hasattr(defender, 'get_armor_bonus') else 0
        damage = max(1, attacker.strength + weapon_bonus - defender.constitution // 2 - armor_bonus)
        defender.current_health -= damage
        self.display_callback(f"{attacker.name} attacks {defender.name} for {damage} damage!\n")

    def defend(self, defender = Character(race=Any, name=Any, gender=Any, job=Any, world_size=Any)):
        defense_boost = defender.constitution // 2
        defender.current_health += defense_boost
        self.display_callback(f"{defender.name} defends and recovers {defense_boost} health!\n")

    def player_turn(self, choice):
        if choice == 'attack':
            self.attack(self.player, self.enemy)
            return "continue"
        elif choice == 'defend':
            self.defend(self.player)
            return "continue"
        elif choice == 'escape':
            self.escape()
            return "escape"

    def enemy_turn(self):
        action = random.choice(["attack", "defend"])
        if action == "attack":
            self.attack(self.enemy, self.player)
        else:
            self.defend(self.enemy)

    def escape(self):
        penalty = 10
        self.player.current_health -= penalty
        self.display_callback(f"{self.player.name} escapes the battle but loses {penalty} health!\n")

    def start_battle(self):
        self.display_callback(f"A wild {self.enemy.name} appears!\n")
        while self.player.current_health > 0 and self.enemy.current_health > 0:
            self.display_health()
            # Combat loop will be managed from the main window
            return "continue"

    def use_skill(self, user = Character(race=Any, name=Any, gender=Any, job=Any, world_size=Any), target, skill_category, skill_name):
        return user.use_skill(skill_category, skill_name, target)
    
    def end_battle(self, result):
        if result == "escape":
            self.display_callback(f"{self.player.name} successfully escaped the battle!\n")
        else:
            self.display_callback(f"{self.player.name} defeated the enemy!\n")

    def is_battle_over(self):
        return self.player.current_health <= 0 or self.enemy.current_health <= 0

    def create_combat(player, enemy, display_callback):
        return Combat(player, enemy, display_callback)

    def create_enemy():
        names = ["Goblin", "Orc", "Troll", "Bandit", "Skeleton"]
        name = random.choice(names)
        enemy = Character(race="Goblin", name=name, gender="Male", job="Warrior", world_size=10)
        enemy.current_health = enemy.max_health  # Ensure enemy has current_health attribute
        return enemy
