import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QTimer

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
        self.update_map_display()
        self.initUI()

    def initUI(self):
        self.map_label = QLabel(self)
        self.map_label.setGeometry(50, 50, 700, 300)

        self.info_label = QLabel(self)
        self.info_label.setGeometry(50, 360, 700, 200)

        self.button_layout = QHBoxLayout()
        
        self.save_button = QPushButton('Save Game', self)
        self.save_button.clicked.connect(self.save_game)

        self.load_button = QPushButton('Load Game', self)
        self.load_button.clicked.connect(self.load_game)

        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.load_button)

        layout = QVBoxLayout()
        layout.addWidget(self.map_label)
        layout.addWidget(self.info_label)
        
        button_container = QWidget()
        button_container.setLayout(self.button_layout)
        layout.addWidget(button_container)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Up:
            self.move_player('n')
        elif key == Qt.Key_Down:
            self.move_player('s')
        elif key == Qt.Key_Left:
            self.move_player('w')
        elif key == Qt.Key_Right:
            self.move_player('e')
        elif key == Qt.Key_I:
            self.interact()

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
        map_desc = self.world.describe_surroundings(x, y)
        self.map_label.setText(f"Player Position: {self.player.position}\n\n{map_desc}")

    def check_for_interaction(self):
        x, y = self.player.position
        cell = self.world.map.map[x][y]
        if cell[0] == 'town':
            self.info_label.setText("You have entered a town. Press 'I' to interact.")
        elif cell[0] == 'dungeon':
            self.info_label.setText("You have found a dungeon. Press 'I' to interact.")
        elif cell[0] == 'treasure':
            self.info_label.setText("You have found a treasure. Press 'I' to interact.")
        else:
            self.info_label.setText("")

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
        self.info_label.setText("Welcome to the town!\n1. Rest\n2. Trade\n3. Learn Skill\n4. Leave")
        self.wait_for_town_choice()

    def wait_for_town_choice(self):
        choice = input("Choose an option: ").strip()
        if choice == '1':
            self.rest()
        elif choice == '2':
            self.trade()
        elif choice == '3':
            self.learn_skill()
        elif choice == '4':
            self.info_label.setText("Leaving the town.")
        else:
            self.info_label.setText("Invalid choice. Please try again.")
            self.wait_for_town_choice()

    def rest(self):
        self.player.restore_health()
        self.info_label.setText(f"{self.player.name}'s health is fully restored to {self.player.current_health}")

    def trade(self):
        self.info_label.setText("Trading...")

    def learn_skill(self):
        self.info_label.setText("Learning a new skill...")

    def enter_dungeon(self):
        self.enemy = create_enemy()
        self.combat = Combat(self.player, self.enemy)
        self.combat.start_battle()

    def find_treasure(self):
        self.info_label.setText("Collecting the treasure...")

    def save_game(self):
        save_game(self.player, self.world)
        self.info_label.setText("Game saved successfully.")

    def load_game(self):
        game_state = load_game()
        if game_state:
            self.player = Character.from_save(game_state["player"])
            self.world = GameWorld.from_save(game_state["world"])
            self.update_map_display()
            self.info_label.setText("Game loaded successfully.")
        else:
            self.info_label.setText("No saved game found.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainGameWindow()
    mainWin.show()
    sys.exit(app.exec_())
