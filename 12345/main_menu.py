from PyQt6.QtCore import QTimer, QPropertyAnimation, QPoint, QEasingCurve, Qt, QObject
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtGui import QFont
import random

class Stone(QObject):  # Add this import: from PyQt6.QtCore import 
    def __init__(self, x, y, color, alpha=255):
        super().__init__()
        self._x = x
        self._y = y
        self.color = color
        self.alpha = alpha
        self.animation = None

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Board properties
        self.board_size = 19
        self.cell_size = 30
        self.stone_radius = 12
        
        # Initialize stones with random positions
        self.stones = []
        self.create_random_stones()
        QTimer.singleShot(100, self.create_random_stones)  # Delay stone creation
        
        # Setup animation timer
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.move_stones)
        self.move_timer.start(2000)  # Move stones every 2 seconds

    def create_random_stones(self):
        # Create some white and black stones
        colors = ['white', 'black']
        for _ in range(10):  # Create 10 stones of each color
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            color = random.choice(colors)
            self.stones.append(Stone(x, y, color))

    def move_stones(self):
        for stone in self.stones:
            # Generate new random target position
            new_x = random.randint(0, self.width())
            new_y = random.randint(0, self.height())
            
            # Create animation for the stone
            animation = QPropertyAnimation(stone, b"pos")
            animation.setDuration(1500)  # 1.5 seconds for movement
            animation.setStartValue(QPoint(stone.x, stone.y))
            animation.setEndValue(QPoint(new_x, new_y))
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            
            # Update stone position when animation is finished
            def update_pos(new_pos, stone=stone):
                stone.x = new_pos.x()
                stone.y = new_pos.y()
                self.update()  # Trigger repaint
            
            animation.valueChanged.connect(update_pos)
            animation.start()
            
            # Store animation reference to prevent garbage collection
            stone.animation = animation

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw dark blue background
        painter.fillRect(self.rect(), QColor('#1f2937'))

        # Draw grid
        pen = QPen(QColor(255, 255, 255, 30))
        pen.setWidth(1)
        painter.setPen(pen)

        # Draw grid lines
        grid_size = 30
        for y in range(0, self.height(), grid_size):
            painter.drawLine(0, y, self.width(), y)
        for x in range(0, self.width(), grid_size):
            painter.drawLine(x, 0, x, self.height())

        # Draw stones
        for stone in self.stones:
            stone_color = QColor(stone.color)
            stone_color.setAlpha(stone.alpha)
            
            painter.setBrush(QBrush(stone_color))
            if stone.color == 'white':
                painter.setPen(QPen(QColor(0, 0, 0, stone.alpha)))
            else:
                painter.setPen(Qt.PenStyle.NoPen)
            
            painter.drawEllipse(
                QPoint(int(stone.x), int(stone.y)),
                self.stone_radius,
                self.stone_radius
            )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust stone positions when window is resized
        for stone in self.stones:
            stone.x = min(stone.x, self.width())
            stone.y = min(stone.y, self.height())


    def init_ui(self):
        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create menu container
        menu_container = QFrame()
        menu_container.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border-radius: 20px;
                margin: 20px;
            }
        """)
        
        # Create menu layout
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.setSpacing(20)
        menu_layout.setContentsMargins(40, 40, 40, 40)

        # Create title
        title = QLabel("Go Game")
        title.setFont(QFont('Segoe UI', 48, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create buttons
        self.start_btn = self.create_menu_button("Start Game")
        self.settings_btn = self.create_menu_button("Settings")
        self.exit_btn = self.create_menu_button("Exit")

        # Add widgets to menu layout
        menu_layout.addWidget(title)
        menu_layout.addSpacing(20)
        menu_layout.addWidget(self.start_btn)
        menu_layout.addWidget(self.settings_btn)
        menu_layout.addWidget(self.exit_btn)

        # Add menu container to main layout
        main_layout.addStretch(1)
        main_layout.addWidget(menu_container)
        main_layout.addStretch(1)

    def create_menu_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        return button