# src/town.py
from typing import Any
from character import Character
import random
from skills import skills
from items import items_for_sale, get_item_by_name

class Town:
    def __init__(self, name):
        self.skills_available = self.randomize_skills()
        self.items_for_sale = self.randomize_items_with_stock()
        self.visitors = []
        self.name = name

    def __repr__(self):
        return f"Town: {self.name}"

    def randomize_skills(self):
        available_skills = [skill for category in skills.values() for skill in category.keys()]
        return random.sample(available_skills, min(5, len(available_skills)))

    def randomize_items_with_stock(self):
        items = random.sample(items_for_sale, min(5, len(items_for_sale)))
        items_with_stock = [{**item, "stock": random.randint(1, 5)} for item in items]
        return items_with_stock

    def add_visitor(self, player):
        self.visitors.append(player)
        print(f"{player.name} has entered the town.")

    def remove_visitor(self, player):
        self.visitors.remove(player)
        print(f"{player.name} has left the town.")

    def display_skills(self):
        print("\nAvailable skills:")
        for skill_name in self.skills_available:
            skill_info = skills[skill_name]
            print(f"{skill_name}: {skill_info['description']}")

    def display_items(self):
        print("\nItems for sale:")
        for item in self.items_for_sale:
            print(f"{item['name']} - {item['price']} gold (Stock: {item['stock']})")

    def learn_skill(self, player, skill_name):
        if skill_name in self.skills_available:
            player.learn_skill(skill_name)
        else:
            print(f"Skill {skill_name} is not available in this town.")

    def buy_item(self, player, item_name = Any):
        for item in self.items_for_sale:
            if item["name"] == item_name:
                if item["stock"] > 0:
                    if player.money >= item["price"]:
                        player.buy_item(item_name)
                        item["stock"] -= 1
                        return True
                    else:
                        print(f"{player.name} does not have enough gold to buy {item_name}.")
                        return False
                else:
                    print(f"{item_name} is out of stock.")
                    return False
        print(f"Item {item_name} is not available for sale in this town.")
        return False

    def sell_item(self, player, item_name):
        for item in player.inventory:
            if item["name"] == item_name:
                for town_item in self.items_for_sale:
                    if town_item["name"] == item_name:
                        town_item["stock"] += 1
                        player.sell_item(item_name)
                        return
                self.items_for_sale.append({"name": item_name, "price": item["price"], "stock": 1})
                player.sell_item(item_name)
                return
        print(f"{item_name} not found in inventory.")

    def visit(self, player):
        player.status = "urban"
        self.add_visitor(player)
        print(f"{player.name} has entered the town.")

    def leave(self, player):
        player.status = "rural"
        self.remove_visitor(player)
        print(f"{player.name} has left the town.")

    def interact(self, player):
        self.visit(player)
        while True:
            print("\nWhat would you like to do?")
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
                self.leave(player)
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
                item_name = input("Enter the name of the item you want to buy: ").strip()
                self.buy_item(player, item_name)
            elif choice == '2':
                item_name = input("Enter the name of the item you want to sell: ").strip()
                self.sell_item(player, item_name)                
            elif choice == '3':
                self.display_items()
            elif choice == '4':
                print("Leaving the market.")
                break
            else:
                print("Invalid choice. Please try again.")

    
# write some code to try this module.


