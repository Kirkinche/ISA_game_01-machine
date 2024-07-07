# src/treasures.py

treasures = [
    {"name": "Gold Coins", "type": "gold", "amount": 50},
    {"name": "Silver Coins", "type": "gold", "amount": 30},
    {"name": "Emerald Necklace", "type": "item", "value": 100},
    {"name": "Magic Ring", "type": "item", "value": 150},
    {"name": "Health Potion", "type": "consumable", "effect": "restore_health", "value": 10}
]

def get_random_treasure():
    import random
    return random.choice(treasures)
