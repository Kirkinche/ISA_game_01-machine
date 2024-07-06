# src/world.py

from procedural_map import Map
from combat import Combat, create_enemy

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
            if not self.interact_dungeon(player):
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
            print("3. Leave")
            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.rest(player)
            elif choice == '2':
                self.trade(player)
            elif choice == '3':
                print("Leaving the town.")
                break
            else:
                print("Invalid choice. Please try again.")

    def rest(self, player):
        print("You rest at the inn. Your health is fully restored.")
        player.restore_health()

    def trade(self, player):
        print("You enter the market to trade.")
        # Add logic for trading (e.g., buying and selling items)

    def interact_dungeon(self, player):
        print("You have found a dungeon. Prepare for battle!")
        enemy = create_enemy()
        combat = Combat(player, enemy)
        return combat.start_battle()

    def interact_treasure(self, player):
        print("You have found a treasure! Your wealth increases.")

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
