import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QRectF, QRect
from PyQt6.QtGui import QPainter, QColor, QBrush, QMovie, QPixmap

class OverlayMedia(QLabel):
    def __init__(self, width, height, gif_infos=[], png_infos=[], parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.gif_infos = gif_infos
        
        self.gifs = [QMovie(path) for path, x, y in gif_infos]
        for gif in self.gifs:
            gif.frameChanged.connect(self.update)
            gif.start()
        
        self.png_infos = png_infos
        self.pixmaps = [QPixmap(path) for path, x, y in png_infos]

    def add_gif(self, gif_info):
        gif = QMovie(gif_info[0])
        gif.frameChanged.connect(self.update)
        gif.start()
        self.gifs.append(gif)
        self.gif_infos.append(gif_info)

    def add_png(self, png_info):
        pixmap = QPixmap(png_info[0])
        self.pixmaps.append(pixmap)
        self.png_infos.append(png_info)
        
    def remove_gif(self, index):
        if 0 <= index < len(self.gifs):
            self.gifs[index].stop()
            del self.gifs[index]
            del self.gif_infos[index]
            self.update()
            
    def remove_png(self, index):
        if 0 <= index < len(self.pixmaps):
            del self.pixmaps[index]
            del self.png_infos[index]
            self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for gif, (_, x, y) in zip(self.gifs, self.gif_infos):
            painter.drawPixmap(x, y, gif.currentPixmap())
        
        for pixmap, (_, x, y) in zip(self.pixmaps, self.png_infos):
            painter.drawPixmap(x, y, pixmap)

    def move_gif(self, gif_index, position):
        if 0 <= gif_index < len(self.gif_infos):
            path, _, _ = self.gif_infos[gif_index]
            x, y = position
            self.gif_infos[gif_index] = (path, x, y)
            self.gifs[gif_index].start()
            self.gifs[gif_index].frameChanged.connect(self.update)
            self.update()

class SpaceObject(QGraphicsItem):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rect = QRectF(0, 0, width, height)
        self.setPos(x, y)
        self.color = color

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(self.color))
        painter.drawRect(self.rect)

class Player(SpaceObject):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, QColor(0, 0, 255))  # Blue player

class Bullet(SpaceObject):
    def __init__(self, x, y):
        super().__init__(x, y, 4, 10, QColor(255, 255, 255))  # White bullet

class Enemy(SpaceObject):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, QColor(255, 0, 0))  # Red enemy

class Meteor(SpaceObject):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, QColor(128, 128, 128))  # Gray meteor

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Space Shooter")
        self.setFixedSize(800, 600)

        #self.overlay = OverlayMedia(800, 600, png_infos=[("player1.png", 400, 400)])
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.overlay = OverlayMedia(200, 200, png_infos=[("player1.png", 400, 500)])
        #self.overlay.add_png("player1.png")
        layout = QVBoxLayout(central_widget)
        
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.bullets = []
        self.enemies = []
        self.meteors = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Left:
            self.move_player(-10)
        elif event.key() == Qt.Key.Key_Right:
            self.move_player(10)
        elif event.key() == Qt.Key.Key_Space:
            self.shoot_bullet()

    def move_player(self, delta_x):
        for png_info in self.overlay.png_infos:
            path, x, y = png_info
            new_x = max(0, min(self.width() - 40, x + delta_x))
            self.overlay.move_gif(self.overlay.png_infos.index(png_info), (new_x, y))

    def game_loop(self):
        self.update_game_objects()

    def update_game_objects(self):
        # Move and remove bullets
        for bullet in self.bullets[:]:
            bullet.moveBy(0, -7)
            if bullet.y() < 0:
                self.scene.removeItem(bullet)
                self.bullets.remove(bullet)

        # Move and remove enemies
        for enemy in self.enemies[:]:
            enemy.moveBy(0, 2)
            if enemy.y() > 600:
                self.scene.removeItem(enemy)
                self.enemies.remove(enemy)

        # Move and remove meteors
        for meteor in self.meteors[:]:
            meteor.moveBy(0, 3)
            if meteor.y() > 600:
                self.scene.removeItem(meteor)
                self.meteors.remove(meteor)

        # Spawn enemies
        if random.randint(1, 60) == 1:
            enemy = Enemy(random.randint(0, 770), 0)
            self.enemies.append(enemy)
            self.scene.addItem(enemy)

        # Spawn meteors
        if random.randint(1, 120) == 1:
            meteor = Meteor(random.randint(0, 780), 0)
            self.meteors.append(meteor)
            self.scene.addItem(meteor)

        # Check for collisions
        player_pixmap = self.overlay.pixmaps[0]
        player_rect = QRectF(self.overlay.png_infos[0][1], self.overlay.png_infos[0][2], player_pixmap.width(), player_pixmap.height())

        for enemy in self.enemies[:]:
            if player_rect.intersects(enemy.boundingRect().translated(enemy.pos())):
                self.game_over()
            for bullet in self.bullets[:]:
                if bullet.boundingRect().translated(bullet.pos()).intersects(enemy.boundingRect().translated(enemy.pos())):
                    self.scene.removeItem(bullet)
                    self.bullets.remove(bullet)
                    self.scene.removeItem(enemy)
                    self.enemies.remove(enemy)
                    break

        for meteor in self.meteors[:]:
            if player_rect.intersects(meteor.boundingRect().translated(meteor.pos())):
                self.game_over()

    def shoot_bullet(self):
        bullet = Bullet(self.overlay.png_infos[0][1] + 18, self.overlay.png_infos[0][2])
        self.bullets.append(bullet)
        self.scene.addItem(bullet)

    def game_over(self):
        self.timer.stop()
        print("Game Over!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec())
