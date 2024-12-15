# src/ui/components/animated_button.py

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class AnimatedButton(QPushButton):
    def __init__(self, text: str, color: str, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(200, 50)
        self.setFont(QFont('Arial', 14))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setStyleSheet(f'''
            QPushButton {{
                background-color: {color};
                border-radius: 25px;
                color: white;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {color.replace('rgb', 'rgba').replace(')', ', 0.8)')};
            }}
        ''')
        
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(200)

    def enterEvent(self, event):
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.pos() + QPoint(0, -5))
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    def leaveEvent(self, event):
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.pos() + QPoint(0, 5))
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()
