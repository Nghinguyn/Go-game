from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QComboBox, QPushButton, QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class UserPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_layout.setSpacing(0)
        
        # Title
        title = QLabel("Player Setup")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 48px;
                margin-bottom: 30px;
            }
        """)
        
        # Players Container
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border-radius: 15px;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 40, 40, 40)
        container_layout.setSpacing(30)
        
        # Player 1
        player1_label = QLabel("Player 1")
        player1_label.setStyleSheet("color: white; font-size: 24px; margin-bottom: 10px;")
        
        name1_label = QLabel("Name:")
        name1_label.setStyleSheet("color: white; font-size: 14px; margin-bottom: 5px;")
        self.player1_name = QLineEdit()
        
        color1_label = QLabel("Color:")
        color1_label.setStyleSheet("color: white; font-size: 14px; margin-bottom: 5px;")
        self.player1_color = QComboBox()
        self.player1_color.addItems(["black", "white"])
        
        # Player 2
        player2_label = QLabel("Player 2")
        player2_label.setStyleSheet("color: white; font-size: 24px; margin-bottom: 10px; margin-top: 20px;")
        
        name2_label = QLabel("Name:")
        name2_label.setStyleSheet("color: white; font-size: 14px; margin-bottom: 5px;")
        self.player2_name = QLineEdit()
        
        color2_label = QLabel("Color:")
        color2_label.setStyleSheet("color: white; font-size: 14px; margin-bottom: 5px;")
        self.player2_color = QComboBox()
        self.player2_color.addItems(["white", "black"])
        
        # Add to container layout
        container_layout.addWidget(player1_label)
        container_layout.addWidget(name1_label)
        container_layout.addWidget(self.player1_name)
        container_layout.addWidget(color1_label)
        container_layout.addWidget(self.player1_color)
        container_layout.addWidget(player2_label)
        container_layout.addWidget(name2_label)
        container_layout.addWidget(self.player2_name)
        container_layout.addWidget(color2_label)
        container_layout.addWidget(self.player2_color)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(20)
        
        self.back_btn = QPushButton("Back to Menu")
        self.start_btn = QPushButton("Start Game")
        
        button_layout.addWidget(self.back_btn)
        button_layout.addWidget(self.start_btn)
        
        # Add all to main layout
        main_layout.addWidget(title)
        main_layout.addWidget(container)
        main_layout.addSpacing(30)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
        # Apply styles
        self.setStyleSheet("""
            QWidget {
                background-color: #1B1B1B;
            }
            QLineEdit {
                background-color: rgba(52, 73, 94, 0.5);
                color: white;
                border: 1px solid #5D6D7E;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
            }
            QComboBox {
                background-color: rgba(52, 73, 94, 0.5);
                color: white;
                border: 1px solid #5D6D7E;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QComboBox QAbstractItemView {
                background-color: #34495E;
                color: white;
                selection-background-color: transparent;
                selection-color: white;
            }
            QPushButton {
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 30px;
                font-size: 16px;
            }
            QPushButton#back_btn {
                background-color: #E74C3C;
            }
            QPushButton#start_btn {
                background-color: #3498DB;
            }
            QPushButton#back_btn:hover {
                background-color: #C0392B;
            }
            QPushButton#start_btn:hover {
                background-color: #2980B9;
            }
        """)
        
        # Set object names for specific styling
        self.back_btn.setObjectName("back_btn")
        self.start_btn.setObjectName("start_btn")
        
        # Connect color selection changes
        self.player1_color.currentTextChanged.connect(self.update_player2_color)
        self.player2_color.currentTextChanged.connect(self.update_player1_color)

    def update_player2_color(self, color):
        self.player2_color.setCurrentText("white" if color == "black" else "black")

    def update_player1_color(self, color):
        self.player1_color.setCurrentText("white" if color == "black" else "black")

    def validate_input(self):
        if not self.player1_name.text() or not self.player2_name.text():
            QMessageBox.warning(self, "Input Error", 
                              "Both players must enter their names!",
                              QMessageBox.StandardButton.Ok)
            return False
        return True

    def get_players_info(self):
        """Get information for both players"""
        player1_info = (self.player1_name.text(), "black")
        player2_info = (self.player2_name.text(), "white")
        return player1_info, player2_info