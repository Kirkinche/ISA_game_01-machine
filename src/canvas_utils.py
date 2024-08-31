from PyQt6.QtWidgets import QLabel, QApplication, QMainWindow
from PyQt6.QtGui import QPainter, QMovie, QPixmap, QTransform
from PyQt6.QtCore import Qt

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
    
    def move_png(self, png_index, position):
        if 0 <= png_index < len(self.png_infos):
            path, x, y = self.png_infos[png_index]
            x, y = position
            self.png_infos[png_index] = (path, x, y)
            self.update()
    #Scaling and Rotation: Add methods for scaling and rotating media elements, the following method gives bad resolutions and create visual defects and artifacts
    def scale_gif(self, gif_index, scale_factor):
        if 0 <= gif_index < len(self.gifs):
            path, x, y = self.gif_infos[gif_index]
            self.gifs[gif_index].setScaledSize(self.gifs[gif_index].currentPixmap().size() * scale_factor)
            self.update()
    
    def scale_png(self, png_index, scale_factor):
        if 0 <= png_index < len(self.pixmaps):
            path, x, y = self.png_infos[png_index]
            self.pixmaps[png_index] = self.pixmaps[png_index].scaled(self.pixmaps[png_index].size() * scale_factor)
            self.update()
    
    def rotate_png(self, png_index, angle):
        if 0 <= png_index < len(self.pixmaps):
            path, x, y = self.png_infos[png_index]
            transform = QTransform().rotate(angle)  # Create a QTransform object
            rotated_pixmap = self.pixmaps[png_index].transformed(transform)  # Apply the transform to the pixmap
            self.pixmaps[png_index] = rotated_pixmap  # Update the pixmap in the list
            self.update()  # Update the widget to redraw

    def rotate_gif(self, gif_index, angle):
        if 0 <= gif_index < len(self.gifs):
            path, x, y = self.gif_infos[gif_index]
            transform = QTransform().rotate(angle)  # Create a QTransform object
            pixmap = self.gifs[gif_index].currentPixmap()  # Get the current frame's pixmap
            rotated_pixmap = pixmap.transformed(transform)  # Apply the transform to the pixmap
            self.gifs[gif_index].setPixmap(rotated_pixmap)  # Set the rotated pixmap to the QMovie
            self.update()  # Update the widget to redraw
            
                   

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Overlay Media Example")
        self.setFixedSize(800, 600)

        self.overlay = OverlayMedia(800, 600, png_infos=[("player1.png", 400, 400)])
        self.setCentralWidget(self.overlay)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.keyPressEvent = self.handle_key_press
        # Initialize the position for the PNG
        self.png_x = 400
        self.png_y = 400

    def handle_key_press(self, event):
        increment = 50
        if event.key() == Qt.Key.Key_Left:
            self.png_x -= increment
            self.png_x = max(0, self.png_x)  # Ensure it doesn't go off-screen
        elif event.key() == Qt.Key.Key_Down:
            self.png_y += increment
            self.png_y = min(self.height() - 100, self.png_y)  # Ensure it doesn't go off-screen
        elif event.key() == Qt.Key.Key_Up:
            self.png_y -= increment
            self.png_y = max(0, self.png_y)  # Ensure it doesn't go off-screen
        elif event.key() == Qt.Key.Key_Right:
            self.png_x += increment
            self.png_x = min(self.width() - 100, self.png_x)  # Ensure it doesn't go off-screen
        self.overlay.move_png(0, (self.png_x, self.png_y))
        #self.overlay.rotate_png(0, 1)  

    

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
