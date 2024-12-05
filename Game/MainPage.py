import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                            QPushButton, QVBoxLayout)
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QPointF
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QPen, QBrush, QPainterPath
import random, math


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), QColor(44, 62, 80))
        
        # Draw Go board pattern
        pen = QPen(QColor(255, 255, 255, 30))
        pen.setWidth(1)
        painter.setPen(pen)
        
        # Draw grid lines
        spacing = 40
        for i in range(0, self.width(), spacing):
            painter.drawLine(i, 0, i, self.height())
        for i in range(0, self.height(), spacing):
            painter.drawLine(0, i, self.width(), i)
            
        # Draw some Go stones as decoration
        stones = [
            (100, 100), (300, 200), (500, 300),
            (200, 400), (600, 150), (400, 450)
        ]
        
        for x, y in stones:
            # Draw stone shadows
            painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x-15, y-15, 34, 34)
            
            # Draw stones (alternating black and white)
            if (x + y) % 2 == 0:
                painter.setBrush(QBrush(QColor(50, 50, 50)))
            else:
                painter.setBrush(QBrush(QColor(240, 240, 240)))
            painter.drawEllipse(x-17, y-17, 34, 34)

class LogoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(120, 120)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw the logo
        center = self.rect().center()
        radius = 50
        
        # Draw outer circle
        painter.setPen(QPen(Qt.GlobalColor.white, 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(center.x() - radius, center.y() - radius, 
                          radius * 2, radius * 2)
        
        # Draw yin-yang style pattern
        painter.setPen(Qt.PenStyle.NoPen)
        path = QPainterPath()
        path.arcMoveTo(center.x() - radius, center.y() - radius, 
                      radius * 2, radius * 2, 90)
        path.arcTo(center.x() - radius, center.y() - radius, 
                  radius * 2, radius * 2, 90, 180)
        painter.fillPath(path, QBrush(Qt.GlobalColor.white))

class AnimatedButton(QPushButton):
    def __init__(self, text, color, parent=None):
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Go Game')
        self.setFixedSize(800, 600)
        
        # Create background widget
        background = BackgroundWidget(self)
        background.setGeometry(0, 0, 800, 600)
        
        # Central widget
        central = QWidget(self)
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        
        # Logo
        logo = LogoWidget()
        
        # Title
        title = QPushButton("Go Game")
        title.setEnabled(False)
        title.setFont(QFont('Arial', 32, QFont.Weight.Bold))
        title.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
            }
        ''')
        
        # Buttons
        start_btn = AnimatedButton("START", "rgb(46, 204, 113)")
        settings_btn = AnimatedButton("SETTINGS", "rgb(52, 152, 219)")
        exit_btn = AnimatedButton("EXIT", "rgb(231, 76, 60)")
        
        # Layout
        layout.addStretch()
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)
        layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(settings_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        # Connect buttons
        start_btn.clicked.connect(lambda: print("Game Starting..."))
        settings_btn.clicked.connect(lambda: print("Opening Settings..."))
        exit_btn.clicked.connect(self.close)


class Stone:
    def __init__(self, x, y, is_black):
        self.pos = QPointF(x, y)
        self.initial_pos = QPointF(x, y)
        self.is_black = is_black
        self.phase = random.uniform(0, 2 * 3.14159)
        self.amplitude = random.uniform(10, 30)
        self.frequency = random.uniform(0.5, 1.5)

    def update(self, time):
        # Vertical floating motion
        self.pos.setY(self.initial_pos.y() + 
                     self.amplitude * math.sin(self.frequency * time + self.phase))

class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.time = 0
        
        # Create floating stones
        self.stones = []
        stone_positions = [
            (100, 100), (300, 200), (500, 300),
            (200, 400), (600, 150), (400, 450),
            (150, 250), (450, 150), (650, 400)
        ]
        
        for pos in stone_positions:
            self.stones.append(Stone(pos[0], pos[1], random.choice([True, False])))
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # 60 FPS approximately
        
    def update_animation(self):
        self.time += 0.016  # Increment time (in seconds)
        for stone in self.stones:
            stone.update(self.time)
        self.update()  # Trigger repaint
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), QColor(44, 62, 80))
        
        # Draw grid
        pen = QPen(QColor(255, 255, 255, 30))
        pen.setWidth(1)
        painter.setPen(pen)
        
        spacing = 40
        for i in range(0, self.width(), spacing):
            painter.drawLine(i, 0, i, self.height())
        for i in range(0, self.height(), spacing):
            painter.drawLine(0, i, self.width(), i)
            
        # Draw floating stones
        for stone in self.stones:
            # Draw shadow
            painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
            painter.setPen(Qt.PenStyle.NoPen)
            shadow_pos = QPointF(stone.pos.x() + 2, stone.pos.y() + 2)
            painter.drawEllipse(shadow_pos, 17, 17)
            
            # Draw stone
            if stone.is_black:
                painter.setBrush(QBrush(QColor(50, 50, 50)))
            else:
                painter.setBrush(QBrush(QColor(240, 240, 240)))
            painter.drawEllipse(stone.pos, 17, 17)
            
        # Draw grid lines

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
