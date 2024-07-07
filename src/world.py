# src/world.py

from procedural_map import Map
from combat import Combat, create_enemy
from items import items_for_sale
from treasures import get_random_treasure
from skills import skills  # Import skills module

class GameWorld:
    def __init__(self, size=10):
        self.size = size
        self.map = Map(size)
        self.map.place_points_of_interest()

    def display_map(self):
        self.map.display_map()

    def interact(self, x, y, player):
        cell = self.map.map[x][y]
        if cell[0] == 'town':
            self.interact_town(player)
        elif cell[0] == 'dungeon':
            result = self.interact_dungeon(player)
            if result == "defeat":
                return False  # Player was defeated
        elif cell[0] == 'treasure':
            self.interact_treasure(player)
        else:
            print("There's nothing of interest here.")
        return True

    def interact_town(self, player):
        while True:
            print("\nYou have entered a town. What would you like to do?")
            print("1. Rest")
            print("2. Trade")
            print("3. Learn Skill")
            print("4. Leave")
            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.rest(player)
            elif choice == '2':
                self.trade(player)
            elif choice == '3':
                self.learn_skill(player)
            elif choice == '4':
                print("Leaving the town.")
                break
            else:
                print("Invalid choice. Please try again.")

    def rest(self, player):
        print("You rest at the inn. Your health is fully restored.")
        player.restore_health()

    def trade(self, player):
        while True:
            print("\nWelcome to the market. What would you like to do?")
            print("1. Buy items")
            print("2. Sell items")
            print("3. View inventory")
            print("4. Leave market")
            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.buy_items(player)
            elif choice == '2':
                self.sell_items(player)
            elif choice == '3':
                self.view_inventory(player)
            elif choice == '4':
                print("Leaving the market.")
                break
            else:
                print("Invalid choice. Please try again.")

    def buy_items(self, player):
        print("\nItems for sale:")
        for item in items_for_sale:
            print(f"{item['name']} - {item['price']} gold")
        item_name = input("Enter the name of the item you want to buy: ").strip()
        player.buy_item(item_name)

    def sell_items(self, player):
        print("\nYour inventory:")
        for item in player.inventory:
            price = item.get("price", "N/A")
            print(f"{item['name']} - {price} gold")
        item_name = input("Enter the name of the item you want to sell: ").strip()
        player.sell_item(item_name)

    def view_inventory(self, player):
        print("\nYour inventory:")
        for item in player.inventory:
            price = item.get("price", "N/A")
            print(f"{item['name']} - {price} gold")
        print(f"Gold: {player.money}")

    def learn_skill(self, player):
        print("\nAvailable skills:")
        for skill_category, skill_list in skills.items():
            for skill_name, skill_info in skill_list.items():
                print(f"{skill_name}: {skill_info['description']}")
        skill_name = input("Enter the name of the skill you want to learn: ").strip()
        player.learn_skill(skill_name)

    def interact_dungeon(self, player):
        print("You have found a dungeon. Prepare for battle!")
        enemy = create_enemy()
        combat = Combat(player, enemy)
        result = combat.start_battle()
        if result == "escape":
            print(f"{player.name} successfully escaped the dungeon.")
        return result

    def interact_treasure(self, player):
        print("You have found a treasure!")
        treasure = get_random_treasure()
        player.collect_treasure(treasure)

    def describe_surroundings(self, x, y):
        directions = {'N': (x-1, y), 'S': (x+1, y), 'E': (x, y+1), 'W': (x, y-1)}
        descriptions = []
        for direction, (dx, dy) in directions.items():
            if 0 <= dx < self.size and 0 <= dy < self.size:
                cell = self.map.map[dx][dy]
                descriptions.append(f"To the {direction}: {cell[0]}")
            else:
                descriptions.append(f"To the {direction}: Out of bounds")
        return "\n".join(descriptions)

    def list_points_of_interest(self):
        points_of_interest = []
        for x in range(self.size):
            for y in range(self.size):
                cell = self.map.map[x][y]
                if cell[0] in ['town', 'dungeon', 'treasure']:
                    points_of_interest.append((cell[0], (x, y)))
        return points_of_interest

    @classmethod
    def from_save(cls, save_data):
        world = cls(size=save_data["size"])
        world.map.map = save_data["map"]
        return world
