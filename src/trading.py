# src/trading.py

def display_items_for_sale(town):
    items_for_sale = town.items_for_sale
    trade_text = "Items for sale:\n"
    for i, item in enumerate(items_for_sale):
        trade_text += f"{i+1}. {item['name']} - {item['price']} gold (Stock: {item['stock']})\n"
    trade_text += "\nEnter the number of the item you want to buy or 'sell' to sell items."
    return trade_text

def process_trade_command(player, town, choice):
    if choice == 'sell':
        return display_inventory(player)
    else:
        try:
            item_index = int(choice) - 1
            if 0 <= item_index < len(town.items_for_sale):
                item_to_buy = town.items_for_sale[item_index]
                if town.buy_item(player, item_to_buy["name"]):
                    return f"You have bought {item_to_buy['name']}."
                else:
                    return "You do not have enough gold or the item is out of stock."
            else:
                return "Invalid item number. Please try again."
        except ValueError:
            return "Invalid input. Please enter a number or 'sell'."

def display_inventory(player):
    inventory_text = "Your inventory:\n"
    for i, item in enumerate(player.inventory):
        inventory_text += f"{i+1}. {item['name']} - {item['price']} gold\n"
    inventory_text += "\nEnter the number of the item you want to sell."
    return inventory_text

def process_sell_command(player, town, choice):
    try:
        item_index = int(choice) - 1
        if 0 <= item_index < len(player.inventory):
            item_to_sell = player.inventory[item_index]
            town.sell_item(player, item_to_sell["name"])
            return f"You have sold {item_to_sell['name']}."
        else:
            return "Invalid item number. Please try again."
    except ValueError:
        return "Invalid input. Please enter a number."
