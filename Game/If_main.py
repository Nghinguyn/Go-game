# If_main.py
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    # Import here instead of at the top
    from MainPage import MainWindow
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
