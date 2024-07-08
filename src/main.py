import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from character import create_character, Character
from world import GameWorld
from save_load import save_game, load_game
from combat import Combat, create_enemy
from town import Town

class MainGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Game Window')
        self.setGeometry(100, 100, 800, 600)
        self.world = GameWorld()
        self.player = create_character("Player", self.world.size)
        self.initUI()
        self.update_map_display()

    def initUI(self):
        self.map_display = QTextEdit(self)
        self.map_display.setReadOnly(True)

        self.context_display = QTextEdit(self)
        self.context_display.setReadOnly(True)

        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter command here...")
        self.command_input.returnPressed.connect(self.process_command)

        layout = QVBoxLayout()
        layout.addWidget(self.map_display)
        layout.addWidget(self.context_display)
        layout.addWidget(self.command_input)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def process_command(self):
        command = self.command_input.text().strip().lower()
        if command in ['n', 's', 'e', 'w']:
            self.move_player(command)
        elif command == 'i':
            self.interact()
        elif command == 'save':
            self.save_game()
        elif command == 'load':
            self.load_game()
        else:
            self.context_display.setText("Invalid command.")
        self.command_input.clear()

    def move_player(self, direction):
        x, y = self.player.position
        if direction == 'n' and x > 0:
            self.player.position = (x - 1, y)
        elif direction == 's' and x < self.world.size - 1:
            self.player.position = (x + 1, y)
        elif direction == 'e' and y < self.world.size - 1:
            self.player.position = (x, y + 1)
        elif direction == 'w' and y > 0:
            self.player.position = (x, y - 1)
        self.update_map_display()
        self.check_for_interaction()

    def update_map_display(self):
        x, y = self.player.position
        map_str = ""
        for i in range(self.world.size):
            for j in range(self.world.size):
                if (i, j) == (x, y):
                    map_str += "P "
                else:
                    map_str += self.world.map.map[i][j][0][0].upper() + " "
            map_str += "\n"
        self.map_display.setText(map_str)
        map_desc = self.world.describe_surroundings(x, y)
        self.context_display.setText(f"Player Position: {self.player.position}\n\n{map_desc}")

    def check_for_interaction(self):
        x, y = self.player.position
        cell = self.world.map.map[x][y]
        if cell[0] == 'town':
            self.context_display.append("You have entered a town. Press 'I' to interact.")
        elif cell[0] == 'dungeon':
            self.context_display.append("You have found a dungeon. Press 'I' to interact.")
        elif cell[0] == 'treasure':
            self.context_display.append("You have found a treasure. Press 'I' to interact.")
        else:
            self.context_display.append("")

    def interact(self):
        x, y = self.player.position
        cell = self.world.map.map[x][y]
        if cell[0] == 'town':
            self.enter_town()
        elif cell[0] == 'dungeon':
            self.enter_dungeon()
        elif cell[0] == 'treasure':
            self.find_treasure()

    def enter_town(self):
        self.town = Town()
        self.context_display.setText("Welcome to the town!\nOptions:\n1. Rest\n2. Trade\n3. Learn Skill\n4. Leave")
        self.command_input.returnPressed.disconnect()
        self.command_input.returnPressed.connect(self.process_town_command)

    def process_town_command(self):
        choice = self.command_input.text().strip().lower()
        if choice == '1':
            self.rest()
        elif choice == '2':
            self.trade()
        elif choice == '3':
            self.learn_skill()
        elif choice == '4':
            self.leave_town()
        else:
            self.context_display.setText("Invalid choice. Please try again.")
        self.command_input.clear()

    def rest(self):
        self.player.restore_health()
        self.context_display.setText(f"{self.player.name}'s health is fully restored to {self.player.current_health}")
        self.enter_town()

    def trade(self):
        self.context_display.setText("Trading...")
        self.enter_town()

    def learn_skill(self):
        self.context_display.setText("Learning a new skill...")
        self.enter_town()

    def leave_town(self):
        self.command_input.returnPressed.disconnect()
        self.command_input.returnPressed.connect(self.process_command)
        self.update_map_display()

    def enter_dungeon(self):
        self.enemy = create_enemy()
        self.combat = Combat(self.player, self.enemy)
        result = self.combat.start_battle()
        self.context_display.setText(f"Combat Result: {result}")
        self.update_map_display()

    def find_treasure(self):
        self.context_display.setText("Collecting the treasure...")
        self.update_map_display()

    def save_game(self):
        save_game(self.player, self.world)
        self.context_display.setText("Game saved successfully.")

    def load_game(self):
        game_state = load_game()
        if game_state:
            self.player = Character.from_save(game_state["player"])
            self.world = GameWorld.from_save(game_state["world"])
            self.update_map_display()
            self.context_display.setText("Game loaded successfully.")
        else:
            self.context_display.setText("No saved game found.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainGameWindow()
    mainWin.show()
    sys.exit(app.exec_())
