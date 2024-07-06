# src/main.py

from character import create_character
from world import GameWorld
from ui import display_main_menu

def move_player(player, direction, world):
    x, y = player.position
    if direction == 'n' and x > 0:
        player.position = (x - 1, y)
    elif direction == 's' and x < world.size - 1:
        player.position = (x + 1, y)
    elif direction == 'e' and y < world.size - 1:
        player.position = (x, y + 1)
    elif direction == 'w' and y > 0:
        player.position = (x, y - 1)
    else:
        print("You can't move in that direction.")
        return
    print(f"New position: {player.position}")
    print(world.describe_surroundings(player.position[0], player.position[1]))

def start_new_game():
    print("Starting a new game...")
    world = GameWorld()
    world_size = world.size
    
    player_name = input("Enter your character's name: ")
    player = create_character(player_name, world_size)
    print(f"Character created: {player}")
    print(f"Starting position: {player.position}")
    print(world.describe_surroundings(player.position[0], player.position[1]))

    print("\nPoints of Interest:")
    pois = world.list_points_of_interest()
    for poi, (x, y) in pois:
        print(f"{poi.title()} at ({x}, {y})")

    while True:
        command = input("Enter a command (move [N/S/E/W], interact, quit, view poi): ").strip().lower()
        if command.startswith("move"):
            parts = command.split()
            if len(parts) == 2 and parts[1] in ["n", "s", "e", "w"]:
                direction = parts[1]
                move_player(player, direction, world)
            else:
                print("Invalid move command. Use 'move N', 'move S', 'move E', or 'move W'.")
        elif command == "interact":
            x, y = player.position
            world.interact(x, y, player)
        elif command == "view poi":
            print("\nPoints of Interest:")
            for poi, (x, y) in pois:
                print(f"{poi.title()} at ({x}, {y})")
        elif command == "quit":
            print("Exiting game. Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

def main():
    while True:
        display_main_menu()
        choice = input("Choose an option: ").strip()
        if choice == '1':
            start_new_game()
        elif choice == '2':
            print("Load game is not implemented yet.")
        elif choice == '3':
            print("Exiting game. Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
