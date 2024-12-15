
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MainGame(QWidget):
    # Define signals at class level
    current_player_changed = pyqtSignal(int)
    captures_changed = pyqtSignal(int, int)
    move_made = pyqtSignal(int, int, int)
    game_reset = pyqtSignal()
    player_passed = pyqtSignal(int)
    return_to_home = pyqtSignal()

    def __init__(self, size=9):
        super().__init__()
        # Initialize game state
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.cell_size = 40
        self.padding = 20
        self.current_player = 1
        self.pass_count = 0
        self.previous_board = None
        self.captured_black = 0
        self.captured_white = 0

        # Set widget properties
        total_size = (self.size + 1) * self.cell_size + 2 * self.padding
        self.setFixedSize(total_size, total_size)
        self.setMouseTracking(True)

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                neighbors.append((new_x, new_y))
        return neighbors

    def get_group(self, x, y):
        color = self.board[y][x]
        if color == 0:
            return set()
        
        group = set([(x, y)])
        stack = [(x, y)]
        
        while stack:
            current_x, current_y = stack.pop()
            for nx, ny in self.get_neighbors(current_x, current_y):
                if self.board[ny][nx] == color and (nx, ny) not in group:
                    group.add((nx, ny))
                    stack.append((nx, ny))
        return group

    def get_liberties(self, group):
        liberties = set()
        for x, y in group:
            for nx, ny in self.get_neighbors(x, y):
                if self.board[ny][nx] == 0:
                    liberties.add((nx, ny))
        return liberties

    def remove_group(self, group):
        count = len(group)
        for x, y in group:
            self.board[y][x] = 0
        return count

    def check_captures(self, x, y):
        captured = 0
        opponent = 3 - self.board[y][x]
        
        for nx, ny in self.get_neighbors(x, y):
            if self.board[ny][nx] == opponent:
                group = self.get_group(nx, ny)
                if not self.get_liberties(group):
                    captured += self.remove_group(group)
        
        return captured

    def is_valid_move(self, x, y):
        if self.board[y][x] != 0:
            return False
            
        self.board[y][x] = self.current_player
        
        if self.previous_board is not None and self.board == self.previous_board:
            self.board[y][x] = 0
            return False
            
        group = self.get_group(x, y)
        has_liberties = bool(self.get_liberties(group))
        
        if not has_liberties:
            will_capture = False
            for nx, ny in self.get_neighbors(x, y):
                if self.board[ny][nx] == 3 - self.current_player:
                    opp_group = self.get_group(nx, ny)
                    if not self.get_liberties(opp_group):
                        will_capture = True
                        break
            
            if not will_capture:
                self.board[y][x] = 0
                return False
        
        self.board[y][x] = 0
        return True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw board background
        painter.fillRect(self.rect(), QColor('#DEB887'))

        # Draw grid lines
        self.draw_grid(painter)
        
        # Draw star points
        self.draw_star_points(painter)
        
        # Draw stones
        self.draw_stones(painter)
        
        # Draw coordinates
        self.draw_coordinates(painter)

    def draw_grid(self, painter):
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(1)
        painter.setPen(pen)

        for i in range(self.size):
            # Vertical lines
            start_x = self.padding + (i + 1) * self.cell_size
            painter.drawLine(start_x, self.padding + self.cell_size,
                           start_x, self.padding + self.size * self.cell_size)
            
            # Horizontal lines
            start_y = self.padding + (i + 1) * self.cell_size
            painter.drawLine(self.padding + self.cell_size, start_y,
                           self.padding + self.size * self.cell_size, start_y)

    def draw_star_points(self, painter):
        star_points = [(2, 2), (2, 6), (4, 4), (6, 2), (6, 6)] if self.size == 9 else [(2, 2), (2, 4), (3, 3), (4, 2), (4, 4)]
        
        for x, y in star_points:
            if self.board[y][x] == 0:
                center_x = self.padding + (x + 1) * self.cell_size
                center_y = self.padding + (y + 1) * self.cell_size
                painter.setBrush(QBrush(Qt.GlobalColor.black))
                painter.drawEllipse(center_x - 3, center_y - 3, 6, 6)

    def draw_stones(self, painter):
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] != 0:
                    self.draw_stone(painter, x, y, self.board[y][x])

    def draw_stone(self, painter, x, y, color):
        center_x = self.padding + (x + 1) * self.cell_size
        center_y = self.padding + (y + 1) * self.cell_size
        stone_size = int(self.cell_size * 0.8)
        half_stone = stone_size // 2

        gradient = QRadialGradient(
            center_x - half_stone/3,
            center_y - half_stone/3,
            stone_size
        )
        
        if color == 1:  # Black stone
            gradient.setColorAt(0, QColor(96, 96, 96))
            gradient.setColorAt(1, QColor(0, 0, 0))
        else:  # White stone
            gradient.setColorAt(0, QColor(255, 255, 255))
            gradient.setColorAt(1, QColor(220, 220, 220))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - half_stone, center_y - half_stone, stone_size, stone_size)

    def draw_coordinates(self, painter):
        painter.setPen(Qt.GlobalColor.black)
        for i in range(self.size):
            # Column coordinates (A-I or A-G)
            x = self.padding + (i + 1) * self.cell_size
            painter.drawText(x - 5, self.padding - 5, chr(65 + i))
            
            # Row coordinates (1-9 or 1-7)
            y = self.padding + (i + 1) * self.cell_size
            painter.drawText(self.padding - 15, y + 5, str(i + 1))

    def mousePressEvent(self, event):
        x = round((event.pos().x() - self.padding - self.cell_size) / self.cell_size)
        y = round((event.pos().y() - self.padding - self.cell_size) / self.cell_size)
        
        if 0 <= x < self.size and 0 <= y < self.size:
            if self.is_valid_move(x, y):
                self.make_move(x, y)

    def make_move(self, x, y):
        self.pass_count = 0
        self.previous_board = [row[:] for row in self.board]
        self.board[y][x] = self.current_player
        
        self.move_made.emit(x, y, self.current_player)
        
        captures = self.check_captures(x, y)
        if self.current_player == 1:
            self.captured_white += captures
        else:
            self.captured_black += captures
        
        self.captures_changed.emit(self.captured_black, self.captured_white)
        self.current_player = 3 - self.current_player
        self.current_player_changed.emit(self.current_player)
        self.update()

    def reset_game(self):
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 1
        self.captured_black = 0
        self.captured_white = 0
        self.previous_board = None
        self.pass_count = 0
        self.update()
        self.game_reset.emit()

    def pass_move(self):
        self.pass_count += 1
        if self.pass_count >= 2:
            self.show_game_end_dialog()
            return
        
        self.player_passed.emit(self.current_player)
        self.current_player = 3 - self.current_player
        self.current_player_changed.emit(self.current_player)
        self.update()

    def show_game_end_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Game Over")
        dialog.setFixedSize(300, 200)
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        
        message = QLabel("Game Over\nTwo consecutive passes")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(dialog.accept)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        layout.addStretch()
        layout.addWidget(message)
        layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        dialog.setLayout(layout)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                border-radius: 15px;
            }
        """)
        
        dialog.exec()
        
        
        
        
# Add this to the end of mainGame.py

class GoGame(QMainWindow):
    returnToHome = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setMinimumSize(1200, 800)
        
        # Initialize game state
        self.player1 = None
        self.player2 = None
        self.game_mode = None
        self.game_settings = None
        self.move_counter = 1
        
        # Create the game board
        self.board = MainGame(9)
        
        # Create UI elements
        self.current_player_label = QLabel("Current Player: Black (○)")
        self.black_captures_label = QLabel("Black Captures: 0")
        self.white_captures_label = QLabel("White Captures: 0")
        self.move_history_label = QLabel("Move History")
        self.move_history_widget = QListWidget()
        
        # Create buttons
        self.Reset_button = QPushButton("Reset")
        self.Pass_button = QPushButton("Pass")
        self.pause_button = QPushButton("Pause")
        self.back_home_button = QPushButton("Back to Home")
        
        # Initialize UI
        self.initUI()
        
        # Connect signals
        self._connect_signals()

    def initUI(self):
        self.setWindowTitle('Go Game')
        self.showFullScreen()
        
        # Set dark theme for main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QFrame {
                background-color: #2c2c2c;
                border-radius: 15px;
            }
        """)

        # Create central widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Left container setup
        left_container = self._setup_left_container()
        
        # Right container with board
        right_container = self._setup_right_container()
        
        # Add containers to main layout
        main_layout.addLayout(left_container)
        main_layout.addWidget(right_container, 1)

    def _setup_left_container(self):
        container = QVBoxLayout()
        container.setSpacing(20)
        
        # Info panel
        info_panel = self._create_info_panel()
        
        # Button frame
        button_frame = self._create_button_frame()
        
        container.addWidget(info_panel)
        container.addWidget(button_frame)
        
        return container

    def _create_info_panel(self):
        panel = QFrame()
        panel.setFixedWidth(300)
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #2c3e50, stop:1 #3498db);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(20)
        
        # Add player information if available
        if self.player1 and self.player2:
            self._add_player_info(layout)
        
        # Add game status information
        layout.addWidget(self.current_player_label)
        layout.addWidget(self.black_captures_label)
        layout.addWidget(self.white_captures_label)
        layout.addWidget(self.move_history_label)
        layout.addWidget(self.move_history_widget)
        
        return panel

    def _create_button_frame(self):
        frame = QFrame()
        frame.setFixedHeight(160)
        frame.setFixedWidth(300)
        frame.setStyleSheet("""
            QFrame {
                background-color: #2c2c2c;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        
        # Button container
        top_buttons = QHBoxLayout()
        top_buttons.setSpacing(10)
        top_buttons.addWidget(self.Pass_button)
        top_buttons.addWidget(self.Reset_button)
        
        layout.addLayout(top_buttons)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.back_home_button)
        
        return frame

    def _setup_right_container(self):
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #2c2c2c;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        container.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Configure board size
        self.board.cell_size = 80
        self.board.padding = 50
        total_size = (self.board.size + 1) * self.board.cell_size + 2 * self.board.padding
        self.board.setFixedSize(total_size, total_size)
        
        layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignCenter)
        
        return container

    def _connect_signals(self):
        self.board.current_player_changed.connect(self.update_current_player)
        self.board.captures_changed.connect(self.update_captures)
        self.board.move_made.connect(self.record_move)
        self.Reset_button.clicked.connect(self.reset_game)
        self.Pass_button.clicked.connect(self.board.pass_move)
        self.pause_button.clicked.connect(self.show_pause_dialog)
        self.back_home_button.clicked.connect(self.go_back_to_home)

    def update_current_player(self, player):
        text = "Current Player: Black (○)" if player == 1 else "Current Player: White (●)"
        self.current_player_label.setText(text)

    def update_captures(self, black_captures, white_captures):
        self.black_captures_label.setText(f"Black Captures: {black_captures}")
        self.white_captures_label.setText(f"White Captures: {white_captures}")

    def record_move(self, x, y, player):
        col = chr(65 + x)
        row = str(y + 1)
        color = "Black" if player == 1 else "White"
        move_text = f"Move {self.move_counter}: {color} - {col}{row}"
        
        item = QListWidgetItem(move_text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        self.move_history_widget.addItem(item)
        self.move_history_widget.scrollToBottom()
        
        self.move_counter += 1

    def reset_game(self):
        self.move_counter = 1
        self.move_history_widget.clear()
        self.board.reset_game()

    def show_pause_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Game Paused")
        dialog.setFixedSize(400, 300)
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        message = QLabel("Game Paused")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
            }
        """)
        
        resume_btn = QPushButton("Resume Game")
        back_home_btn = QPushButton("Back to Home")
        
        for btn in [resume_btn, back_home_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 15px 30px;
                    min-width: 200px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
        
        resume_btn.clicked.connect(dialog.accept)
        back_home_btn.clicked.connect(lambda: self.return_to_main_menu(dialog))
        
        layout.addStretch()
        layout.addWidget(message)
        layout.addWidget(resume_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(back_home_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        dialog.setLayout(layout)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                border-radius: 20px;
            }
        """)
        
        dialog.exec()

    def go_back_to_home(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirm Exit")
        dialog.setFixedSize(400, 250)
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        message = QLabel("Are you sure you want to return to the home page?")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        
        yes_btn = QPushButton("Yes, Exit")
        no_btn = QPushButton("No, Stay")
        
        for btn, color in [(yes_btn, "#e74c3c"), (no_btn, "#3498db")]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 12px 25px;
                    min-width: 120px;
                }}
            """)
        
        yes_btn.clicked.connect(lambda: self.return_to_main_menu(dialog))
        no_btn.clicked.connect(dialog.reject)
        
        button_container = QHBoxLayout()
        button_container.addWidget(no_btn)
        button_container.addWidget(yes_btn)
        
        layout.addStretch()
        layout.addWidget(message)
        layout.addLayout(button_container)
        layout.addStretch()
        
        dialog.setLayout(layout)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
                border-radius: 20px;
            }
        """)
        
        dialog.exec()

    def return_to_main_menu(self, dialog):
        dialog.accept()
        self.hide()
        self.returnToHome.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        super().keyPressEvent(event)