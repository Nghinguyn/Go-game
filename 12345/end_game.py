from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class EndGameOverlay(QWidget):
    def __init__(self, winner, final_score, move_history, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui(winner, final_score)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
    def init_ui(self, winner, final_score):
        self.setFixedSize(500, 800)
        
        if self.parent:
            parent_geometry = self.parent.geometry()
            x = parent_geometry.center().x() - self.width() // 2
            y = parent_geometry.center().y() - self.height() // 2
            self.move(x, y)
        
        # Main container frame
        main_frame = QFrame(self)
        main_frame.setObjectName("mainFrame")
        main_frame.setGeometry(0, 0, 500, 500)
        main_frame.setStyleSheet("""
            QFrame#mainFrame {
                background-color: #2c3e50;
                border-radius: 20px;
                border: 2px solid #3498db;
            }
        """)
        
        layout = QVBoxLayout(main_frame)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Content container
        content_container = QFrame()
        content_container.setStyleSheet("""
            QFrame {
                background-color: rgba(52, 152, 219, 0.2);
                border-radius: 15px;
            }
            QLabel {
                background: transparent;
                border: none;
            }
        """)
        
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(15)
        
        # Winner announcement
        trophy_label = QLabel("🏆")
        trophy_label.setFont(QFont('Segoe UI', 48))
        trophy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trophy_label.setStyleSheet("color: white; border: none;")
        
        winner_text = QLabel(f"{winner} Wins!")
        winner_text.setFont(QFont('Segoe UI', 36, QFont.Weight.Bold))
        winner_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        winner_text.setStyleSheet("color: white; border: none;")
        
        # Single shadow effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setOffset(0, 0)
        glow.setColor(QColor('#3498db'))
        winner_text.setGraphicsEffect(glow)
        
        # Score display
        score_text = QLabel(f"Final Score\nBlack: {final_score['black']} | White: {final_score['white']}")
        score_text.setFont(QFont('Segoe UI', 18))
        score_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        score_text.setStyleSheet("color: white; border: none;")
        
        content_layout.addWidget(trophy_label)
        content_layout.addWidget(winner_text)
        content_layout.addWidget(score_text)
        
        # Buttons
        button_container = QFrame()
        button_container.setStyleSheet("background: transparent; border: none;")
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)
        
        # Button styling
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        
        self.menu_btn = QPushButton("← Back to Menu")
        self.replay_btn = QPushButton("↺ Replay Game")
        
        for btn in [self.menu_btn, self.replay_btn]:
            btn.setStyleSheet(button_style)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(0, 0, 0, 80))
            btn.setGraphicsEffect(shadow)
            btn.setFixedWidth(200)
        
        button_layout.addWidget(self.menu_btn)
        button_layout.addWidget(self.replay_btn)
        
        # Add all components to main layout
        layout.addWidget(content_container)
        layout.addWidget(button_container)