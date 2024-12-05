import sys
from PyQt6.QtWidgets import QApplication
from main import GoGame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GoGame()
    game.show()
    sys.exit(app.exec())