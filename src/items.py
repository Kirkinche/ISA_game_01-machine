# src/items.py

items_for_sale = [
    {"name": "Health Potion", "type": "consumable", "price": 10, "effect": "restore_health"},
    {"name": "Iron Sword", "type": "weapon", "price": 50, "bonus": 10},
    {"name": "Leather Armor", "type": "armor", "price": 30, "bonus": 5},
    # Add more items as needed
    {"name": "Emerald Necklace", "type": "item", "price": 100},
    {"name": "Magic Ring", "type": "item", "price": 150},
    ]

def get_item_by_name(name):
    for item in items_for_sale:
        if item["name"] == name:
            return item
    return None

class Item:
    def __init__(self, name, type, price, bonus):
        self.name = name
        self.type = type
        self.price = price
        self.bonus = bonus

    def use(self, player):
        if self.type == "consumable":
            self.effect(player)
        elif self.type == "weapon":
            player.inventory.append(self)
        elif self.type == "armor":
            player.inventory.append(self)
        elif self.type == "money":
            player.money += self.price
        elif self.type == "item":
            player.inventory.append(self)
        else:
            print("Invalid item type.")

class Consumable(Item):
    def __init__(self, name, type, price, effect):
        super().__init__(name, type, price)
        self.effect = effect


