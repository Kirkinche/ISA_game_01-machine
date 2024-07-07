# src/town.py

import random
from skills import skills
from items import items_for_sale

class Town:
    def __init__(self):
        self.skills_available = self.randomize_skills()
        self.items_for_sale = self.randomize_items_with_stock()
        self.visitors = []

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
            for skill_category in skills.values():
                if skill_name in skill_category:
                    skill_info = skill_category[skill_name]
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

    def buy_item(self, player, item_name):
        for item in self.items_for_sale:
            if item["name"] == item_name:
                if item["stock"] > 0:
                    if player.money >= item["price"]:
                        player.buy_item(item_name)
                        item["stock"] -= 1
                        return
                    else:
                        print(f"{player.name} does not have enough gold to buy {item_name}.")
                        return
                else:
                    print(f"{item_name} is out of stock.")
                    return
        print(f"Item {item_name} is not available for sale in this town.")

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
