import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QLineEdit
from character import create_character, Character
from world import GameWorld
from save_load import save_game, load_game
from combat import Combat
from town import Town
import trading
import skills as skills_module

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
        self.map_display.setGeometry(50, 50, 700, 300)



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
        elif command == 'view places':
            self.view_places()
        elif command == 'view skills':
            self.context_display.setText(skills_module.display_skills(self.player))
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
        self.update_context_display()

    def update_context_display(self):
        x, y = self.player.position
        map_desc = self.world.describe_surroundings(x, y)
        cell = self.world.map.map[x][y]
        context_text = f"Player Position: {self.player.position}\n\n{map_desc}\n"

        if cell[0] == 'town':
            context_text += "You have entered a town. Available commands: 'i' to interact, 'view places', 'view skills', 'save' to save game, 'load' to load game.\n"
        elif cell[0] == 'dungeon':
            context_text += "You have found a dungeon. Available commands: 'i' to interact, 'view places', 'view skills', 'save' to save game, 'load' to load game.\n"
        elif cell[0] == 'treasure':
            context_text += "You have found a treasure. Available commands: 'i' to interact, 'view places', 'view skills', 'save' to save game, 'load' to load game.\n"
        else:
            context_text += "Available commands: 'n', 's', 'e', 'w' to move, 'view skills', 'save' to save game, 'load' to load game.\n"

        self.context_display.setText(context_text)

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
            self.context_display.setText(trading.display_items_for_sale(self.town))
            self.command_input.returnPressed.disconnect()
            self.command_input.returnPressed.connect(self.process_trade_command)
        elif choice == '3':
            self.context_display.setText(skills_module.display_skills_to_learn(self.town))
            self.command_input.returnPressed.disconnect()
            self.command_input.returnPressed.connect(self.process_learn_skill_command)
        elif choice == '4':
            self.leave_town()
        else:
            self.context_display.setText("Invalid choice. Please try again.")
        self.command_input.clear()

    def rest(self):
        self.player.restore_health()
        self.context_display.setText(f"{self.player.name}'s health is fully restored to {self.player.current_health}")
        self.enter_town()

    def process_trade_command(self):
        choice = self.command_input.text().strip().lower()
        result = trading.process_trade_command(self.player, self.town, choice)
        self.context_display.setText(result)
        self.command_input.clear()
        self.enter_town()

    def process_sell_command(self):
        choice = self.command_input.text().strip().lower()
        result = trading.process_sell_command(self.player, self.town, choice)
        self.context_display.setText(result)
        self.command_input.clear()
        self.enter_town()

    def process_learn_skill_command(self):
        choice = self.command_input.text().strip()
        result = skills_module.process_learn_skill_command(self.player, self.town, choice)
        self.context_display.setText(result)
        self.command_input.clear()
        self.enter_town()

    def leave_town(self):
        self.command_input.returnPressed.disconnect()
        self.command_input.returnPressed.connect(self.process_command)
        self.update_map_display()

    def enter_dungeon(self):
        self.enemy = Combat.create_enemy()
        self.combat = Combat(self.player, self.enemy, self.append_output)
        self.context_display.setText("You have encountered an enemy! Available commands: 'attack', 'defend', 'escape'")
        self.command_input.returnPressed.disconnect()
        self.command_input.returnPressed.connect(self.process_combat_command)

    def process_combat_command(self):
        command = self.command_input.text().strip().lower()
        if command in ['attack', 'defend', 'escape']:
            result = self.combat.player_turn(command)
            if result == "escape":
                self.context_display.setText("You have successfully escaped.")
                self.command_input.returnPressed.disconnect()
                self.command_input.returnPressed.connect(self.process_command)
                self.update_map_display()
                return
            self.combat.display_health()
            if self.enemy.current_health <= 0:
                self.context_display.append("You have defeated the enemy!")
                self.command_input.returnPressed.disconnect()
                self.command_input.returnPressed.connect(self.process_command)
                self.update_map_display()
                return
            self.combat.enemy_turn()
            self.combat.display_health()
            if self.player.current_health <= 0:
                self.context_display.append("You have been defeated...")
                self.command_input.returnPressed.disconnect()
                self.command_input.returnPressed.connect(self.process_command)
                self.update_map_display()
                return
            self.context_display.append("Combat continues. Available commands: 'attack', 'defend', 'escape'")
        else:
            self.context_display.setText("Invalid command. Available commands: 'attack', 'defend', 'escape'")
        self.command_input.clear()

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

    def view_places(self):
        x, y = self.player.position
        cell = self.world.map.map[x][y]
        if cell[0] == 'town':
            self.context_display.setText("Places of interest in the town:\n1. Inn\n2. Market\n3. Training Ground")
        elif cell[0] == 'dungeon':
            self.context_display.setText("Features of the dungeon:\n1. Dark Hallways\n2. Hidden Traps\n3. Monster Lairs")
        elif cell[0] == 'treasure':
            self.context_display.setText("Details about the treasure:\n1. Ancient Artifacts\n2. Precious Gems\n3. Gold Coins")
        else:
            self.context_display.setText("No special places here.")

    def view_skills(self):
        if not self.player.skills:
            self.context_display.setText("You have not learned any skills yet.")
        else:
            skills_text = "Your skills:\n"
            for skill in self.player.skills:
                skill_info = skills[skill]
                skills_text += f"{skill}: {skill_info['description']}\n"
            self.context_display.setText(skills_text)

    def append_output(self, text):
        self.context_display.append(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainGameWindow()
    mainWin.show()
    sys.exit(app.exec_())
