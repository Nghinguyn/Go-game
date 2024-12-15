
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, QTimer, QPointF
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QPen, QBrush, QPainterPath, QRadialGradient
from Setting import SettingsDialog
from UserPage import UserPageDialog
from mainGame import GoGame
import random, math


class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_PaintOnScreen)


        self.setUpdatesEnabled(True)
        
        # Initialize with default positions first
        self.stones = []
        self.lower()
        
        # Set up 120fps timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(1000 // 120)  # 120 FPS (approximately 8.33ms per frame)
        self.time = 0.0
        self.delta_time = 1.0 / 120.0  # Time delta for 120fps
        
        # Initial size
        self.setMinimumSize(800, 600)


    
            
    def showEvent(self, event):
        super().showEvent(event)
        if not self.stones:
            for _ in range(20):  # Reduced number of stones
                x = random.randint(30, max(30, self.width() - 30))
                y = random.randint(30, max(30, self.height() - 30))
                is_black = random.choice([True, False])
                self.stones.append(Stone(x, y, is_black))
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Redistribute stones when window is resized
        if self.stones:  # Only redistribute if we have stones
            for stone in self.stones:
                stone.pos = QPointF(
                    random.randint(30, max(30, self.width() - 30)),
                    random.randint(30, max(30, self.height() - 30))
                )
        
    def update_animation(self):
        self.time += self.delta_time
        for stone in self.stones:
            stone.update(self.time)
        self.update()  # Trigger repaint

        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        
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
            
        # Draw animated stones
        for stone in self.stones:
            x = stone.pos.x()
            y = stone.pos.y()
            
            # Draw stone shadow
            painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(x-15), int(y-15), 34, 34)
            
            # Draw stone
            color = QColor(50, 50, 50) if stone.is_black else QColor(240, 240, 240)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(x-17), int(y-17), 34, 34)

            self.draw_stone(painter, stone.pos.x(), stone.pos.y(), stone.is_black)

    def draw_stone(self, painter, x, y, is_black):
        # Create gradients for the stone
        if is_black:
            gradient = QRadialGradient(x-5, y-5, 20)
            gradient.setColorAt(0, QColor(80, 80, 80))
            gradient.setColorAt(0.5, QColor(20, 20, 20))
            gradient.setColorAt(1, QColor(0, 0, 0))
        else:
            gradient = QRadialGradient(x-5, y-5, 20)
            gradient.setColorAt(0, QColor(255, 255, 255))
            gradient.setColorAt(0.5, QColor(240, 240, 240))
            gradient.setColorAt(1, QColor(210, 210, 210))

        # Draw shadow with blur effect
        shadow_gradient = QRadialGradient(x+2, y+2, 19)
        shadow_gradient.setColorAt(0, QColor(0, 0, 0, 60))
        shadow_gradient.setColorAt(1, QColor(0, 0, 0, 10))
        painter.setBrush(shadow_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(x-15), int(y-15), 34, 34)

        # Draw the stone with gradient
        painter.setBrush(gradient)
        painter.drawEllipse(int(x-17), int(y-17), 34, 34)

        # Add highlight/reflection
        highlight = QPainterPath()
        highlight.addEllipse(QPointF(x-7, y-7), 8, 8)
        painter.setBrush(QColor(255, 255, 255, 90))
        painter.drawPath(highlight)


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
        # Initialize default settings
        self.board_size = 19  # Default board size
        self.sound_enabled = True
        self.game_timer = 5
        self.game_board = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Go Game')
        self.showFullScreen()
        
        # Create stacked widget to manage different screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create menu screen
        self.menu_screen = QWidget()
        menu_layout = QVBoxLayout(self.menu_screen)
        
        # Background for menu
        self.background = BackgroundWidget(self.menu_screen)
        self.background.setGeometry(0, 0, self.width(), self.height())
        
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
        menu_layout.addStretch()
        menu_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        menu_layout.addSpacing(30)
        menu_layout.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(settings_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(exit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        menu_layout.addStretch()
        
        # Create game screen
        self.game_screen = GameBoard()
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.menu_screen)
        self.stacked_widget.addWidget(self.game_screen)
        
        # Connect buttons
        start_btn.clicked.connect(self.show_user_page)
        settings_btn.clicked.connect(self.show_settings)
        exit_btn.clicked.connect(QApplication.instance().quit)
        
        
        # Create background widget first
        self.background = BackgroundWidget(self.menu_screen)
        self.background.setGeometry(0, 0, self.width(), self.height())
        
        # Create logo and buttons AFTER background
        # This ensures they're created on top of the background
        self.logo = QLabel(self.menu_screen)
        # ... logo setup ...



        
        
        
        

    def show_user_page(self):
        if not self.game_board:
            self.game_board = GoGame()
            self.game_board.returnToHome.connect(self.show_menu)  # Connect the signal
        
        self.user_dialog = UserPageDialog(self, self.game_board)
        self.user_dialog.game_started.connect(self.start_game)
        self.user_dialog.show()


    def start_game(self, game_settings):
        """Handle game start with player settings"""
        try:
            print(f"Starting game with settings: {game_settings}")
            
            # Create new game board with settings
            self.game_board.setup_game(game_settings)
            
            self.stacked_widget.setCurrentWidget(self.game_board)
            
        except Exception as e:
            print(f"Error in start_game: {e}")
            QMessageBox.critical(self, "Error", "Failed to start game. Please try again.")


    def show_settings(self):
        settings_dialog = SettingsDialog(self)
        settings_dialog.settings_changed.connect(self.apply_settings)
        settings_dialog.exec()

    def apply_settings(self, settings):
        # Apply the settings from the settings dialog
        pass


    def start_game_board(self):
        # Clear any existing game state
        if hasattr(self, 'game_board'):
            self.game_board.close()
        
        # Initialize the game board with current settings
        self.game_board = GameBoard(
            player1=self.player1,
            player2=self.player2,
            mode=self.current_game_mode,
            # Add other necessary parameters
            parent=self
        )
        
        # Show the game board
        self.setCentralWidget(self.game_board)
        self.game_board.show()


    def show_menu(self):
        """Switch back to the menu screen"""
        self.stacked_widget.setCurrentIndex(0)



class GameBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stones = {}  # Dictionary to store placed stones
        self.grid_size = 40
        self.board_size = 19
        self.black_turn = True
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw game board
        offset_x = (self.width() - (self.board_size - 1) * self.grid_size) // 2
        offset_y = (self.height() - (self.board_size - 1) * self.grid_size) // 2
        
        # Draw game grid
        pen = QPen(QColor(255, 255, 255, 100))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for i in range(self.board_size):
            x = offset_x + i * self.grid_size
            y = offset_y + i * self.grid_size
            painter.drawLine(x, offset_y, x, offset_y + (self.board_size - 1) * self.grid_size)
            painter.drawLine(offset_x, y, offset_x + (self.board_size - 1) * self.grid_size, y)
        
        # Draw placed stones
        for (x, y), is_black in self.stones.items():
            stone_x = offset_x + x * self.grid_size
            stone_y = offset_y + y * self.grid_size
            
            # Draw shadow
            painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(stone_x + 2, stone_y + 2, 34, 34)
            
            # Draw stone
            color = QColor(50, 50, 50) if is_black else QColor(240, 240, 240)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(stone_x - 17, stone_y - 17, 34, 34)


        for (x, y), is_black in self.stones.items():
            stone_x = offset_x + x * self.grid_size
            stone_y = offset_y + y * self.grid_size
            self.draw_stone(painter, stone_x, stone_y, is_black)

    def mousePressEvent(self, event):
        offset_x = (self.width() - (self.board_size - 1) * self.grid_size) // 2
        offset_y = (self.height() - (self.board_size - 1) * self.grid_size) // 2
        
        # Calculate grid position
        x = round((event.position().x() - offset_x) / self.grid_size)
        y = round((event.position().y() - offset_y) / self.grid_size)
        
        # Check if click is within board bounds
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            # Place stone if intersection is empty
            if (x, y) not in self.stones:
                self.stones[(x, y)] = self.black_turn
                self.black_turn = not self.black_turn
                self.update()


    def set_board_size(self, size):
        self.board_size = size
        self.stones.clear()  # Clear stones when board size changes
        self.update()



class Stone:
    SPEED_MULTIPLIER = 0.3
    GRID_SIZE = 40
    MAX_STEPS = 1

    def __init__(self, x, y, is_black):
        self.original_grid_x = round(x / self.GRID_SIZE)
        self.original_grid_y = round(y / self.GRID_SIZE)
        self.is_black = is_black
        
        self.pos = QPointF(x, y)
        self.velocity = QPointF(0, 0)
        
        # Movement parameters
        self.direction = random.uniform(0, 2 * math.pi)
        self.speed = 0.5  # Base movement speed
        
        # Boundary box (area where stone can move)
        self.min_x = x - self.GRID_SIZE * self.MAX_STEPS
        self.max_x = x + self.GRID_SIZE * self.MAX_STEPS
        self.min_y = y - self.GRID_SIZE * self.MAX_STEPS
        self.max_y = y + self.GRID_SIZE * self.MAX_STEPS
        
        # Direction change parameters
        self.direction_timer = 0
        self.direction_change_interval = random.uniform(2.0, 4.0)

    def update(self, time):
        # Update direction periodically
        self.direction_timer += time
        if self.direction_timer >= self.direction_change_interval:
            self.direction_timer = 0
            self.direction_change_interval = random.uniform(2.0, 4.0)
            # Gradual direction change
            self.direction += random.uniform(-0.5, 0.5)  # Small random direction change
            
        # Calculate new position
        dx = math.cos(self.direction) * self.speed
        dy = math.sin(self.direction) * self.speed
        
        new_x = self.pos.x() + dx
        new_y = self.pos.y() + dy
        
        # Bounce off boundaries
        if new_x < self.min_x or new_x > self.max_x:
            dx = -dx
            self.direction = math.pi - self.direction
        if new_y < self.min_y or new_y > self.max_y:
            dy = -dy
            self.direction = -self.direction
            
        # Update position
        self.pos = QPointF(
            max(self.min_x, min(self.max_x, self.pos.x() + dx)),
            max(self.min_y, min(self.max_y, self.pos.y() + dy))
        )


    




