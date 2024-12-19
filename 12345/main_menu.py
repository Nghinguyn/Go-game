from PyQt6.QtCore import QTimer, QPropertyAnimation, QPoint, QEasingCurve, Qt, QObject, pyqtProperty
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QFrame,
                            QDialog, QScrollArea)
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont
import random

class Stone(QObject):
    def __init__(self, x, y, color, alpha=255):
        super().__init__()
        self._pos = QPoint(x, y)
        self.color = color
        self.alpha = alpha
        self.animation = None

    @pyqtProperty(QPoint)
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value

    # Add x and y properties with setters
    @property
    def x(self):
        return self._pos.x()

    @x.setter
    def x(self, value):
        self._pos = QPoint(value, self._pos.y())

    @property
    def y(self):
        return self._pos.y()

    @y.setter
    def y(self, value):
        self._pos = QPoint(self._pos.x(), value)

    # Method to update position
    def set_position(self, x, y):
        self._pos = QPoint(x, y)

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
            animation.setDuration(1500)
            animation.setStartValue(stone.pos)
            animation.setEndValue(QPoint(new_x, new_y))
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            
            # Update stone position when animation is finished
            def update_pos(new_pos):
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
            
            pos = stone.pos  # Use the pos property
            painter.drawEllipse(
                pos,
                self.stone_radius,
                self.stone_radius
            )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adjust stone positions when window is resized
        for stone in self.stones:
            new_x = min(stone.x, self.width())
            new_y = min(stone.y, self.height())
            stone.set_position(new_x, new_y)


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

        # Create "How to Play" as a clickable label
        self.how_to_play_label = QLabel("How to Play")
        self.how_to_play_label.setFont(QFont('Time New Roman', 24))
        # Add underline to the font
        font = self.how_to_play_label.font()
        font.setUnderline(True)
        self.how_to_play_label.setFont(font)
        self.how_to_play_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                padding: 5px;
            }
            QLabel:hover {
                color: white;
            }
        """)
        self.how_to_play_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.how_to_play_label.mousePressEvent = self.show_how_to_play
        # Make the label interactive
        self.how_to_play_label.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create buttons
        self.start_btn = self.create_menu_button("Start Game")
        self.settings_btn = self.create_menu_button("Settings")
        self.exit_btn = self.create_menu_button("Exit")

        # Add widgets to menu layout
        menu_layout.addWidget(title)
        menu_layout.addSpacing(20)
        menu_layout.addWidget(self.how_to_play_label)  # Add How to Play text first
        menu_layout.addWidget(self.start_btn)          # Then Start Game button
        menu_layout.addWidget(self.settings_btn)
        menu_layout.addWidget(self.exit_btn)

        # Add menu container to main layout
        main_layout.addStretch(1)
        main_layout.addWidget(menu_container)
        main_layout.addStretch(1)

    def show_how_to_play(self, event=None):  # Add event parameter for mousePressEvent
        self.rules_dialog = HowToPlayDialog()
        # Center the dialog on the screen
        screen = self.screen().geometry()
        self.rules_dialog.move(
            screen.center() - self.rules_dialog.rect().center()
        )
        self.rules_dialog.show()

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
    
    
class HowToPlayDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("How to Play Go")
        self.setFixedSize(600, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                color: white;
            }
            QLabel {
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                border: none;
                border-radius: 5px;
                padding: 10px;
                min-width: 100px;
                color: white;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("How to Play Go")
        title.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Rules text
        rules_text = """
        <h3>Basic Rules:</h3>
        <p>1. Players take turns placing stones on board intersections</p>
        <p>2. Black plays first</p>
        <p>3. Stones must have at least one liberty (empty adjacent intersection) to survive</p>
        
        <h3>Capturing Stones:</h3>
        <p>• Surround opponent's stones completely to capture them</p>
        <p>• Captured stones are removed from the board</p>
        
        <h3>Game End:</h3>
        <p>• Game ends when both players pass consecutively</p>
        <p>• Territory is counted: empty intersections surrounded by your stones</p>
        <p>• Winner has the most territory plus captured stones</p>
        
        <h3>Controls:</h3>
        <p>• Click to place stones</p>
        <p>• Use the Pass button when you can't/don't want to move</p>
        <p>• Timer shows remaining time for each player</p>
        """

        rules_label = QLabel(rules_text)
        rules_label.setWordWrap(True)
        rules_label.setTextFormat(Qt.TextFormat.RichText)

        # Close button
        close_btn = QPushButton("Got it!")
        close_btn.clicked.connect(self.close)
        close_btn.setFixedWidth(200)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(rules_label)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)