from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QMovie, QPixmap
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
