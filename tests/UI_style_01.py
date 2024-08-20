import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        # Top two main panels
        topLayout = QHBoxLayout()
        self.mapPanel = QFrame()
        self.mapPanel.setFrameShape(QFrame.Shape.StyledPanel)
        self.contextPanel = QFrame()
        self.contextPanel.setFrameShape(QFrame.Shape.StyledPanel)
        topLayout.addWidget(self.mapPanel)
        topLayout.addWidget(self.contextPanel)
        mainLayout.addLayout(topLayout)

        # Middle bar
        self.middleBar = QFrame()
        self.middleBar.setFrameShape(QFrame.Shape.StyledPanel)
        self.middleBar.setFixedHeight(30)
        mainLayout.addWidget(self.middleBar)

        # Bottom five small panels
        bottomLayout = QHBoxLayout()
        for _ in range(5):
            panel = QFrame()
            panel.setFrameShape(QFrame.Shape.StyledPanel)
            panel.setFixedSize(100, 100)
            bottomLayout.addWidget(panel)
            # Create a QLabel and add it to the panel
            label = QLabel("Panel " + str(_ + 1))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            panel.layout = QVBoxLayout(panel)
            panel.layout.addWidget(label)

        mainLayout.addLayout(bottomLayout)
        
        



        self.setLayout(mainLayout)
        self.setWindowTitle('Sample Layout')
        self.setGeometry(100, 100, 800, 600)


def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
