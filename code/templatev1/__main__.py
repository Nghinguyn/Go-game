import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from board import Board

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Board Test")
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.setGeometry(100, 100, 600, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
