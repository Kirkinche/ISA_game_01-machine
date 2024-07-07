# src/items.py

items_for_sale = [
    {"name": "Health Potion", "type": "consumable", "price": 10, "effect": "restore_health"},
    {"name": "Iron Sword", "type": "weapon", "price": 50, "bonus": 10},
    {"name": "Leather Armor", "type": "armor", "price": 30, "bonus": 5}
]

def get_item_by_name(name):
    for item in items_for_sale:
        if item["name"] == name:
            return item
    return None
