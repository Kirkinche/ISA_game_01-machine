# src/ui.py

def display_main_menu():
    print("1. Start New Game")
    print("2. Load Game")
    print("3. Exit")

def display_character_creation():
    print("Character Creation:")
    print("1. Race: Human, Elf, Dwarf")
    print("2. Gender: Male, Female")
    print("3. Job: Warrior, Mage, Rogue")

def display_game_info(player, world):
    print(f"Player: {player}")
    print(f"World Size: {world.size}")
    print(f"Points of Interest: {world.list_points_of_interest()}")

def display_combat_options():
    print("Combat Options:")
    print("1. Attack")
    print("2. Defend")
    print("3. Escape")

def display_town_options():
    print("Town Options:")
    print("1. Rest")
    print("2. Trade")
    print("3. Learn Skill")
    print("4. Leave")

def display_skills(skills_available):
    print("Available Skills:")
    for skill_name in skills_available:
        skill_info = skills[skill_name]
        print(f"{skill_name}: {skill_info['description']}")

def display_items_for_sale(items_for_sale):
    print("Items for sale:")
    for item in items_for_sale:
        print(f"{item['name']} - {item['price']} gold")

def display_inventory(inventory):
    print("Your inventory:")
    for item in inventory:
        print(f"{item['name']}")