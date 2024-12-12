
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *



class MainGame(QWidget):

    current_player_changed = pyqtSignal(int)
    captures_changed = pyqtSignal(int, int)  # Move this to class level
    move_made = pyqtSignal(int, int, int)  # Add new signal (x, y, player)
    game_reset = pyqtSignal()  # Signal for game reset
    player_passed = pyqtSignal(int)  # Signal for when a player passes
    return_to_home = pyqtSignal()



    def __init__(self, size=9):
        super().__init__()
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.cell_size = 40
        self.padding = 20
        self.current_player = 1
        self.pass_count = 0

        total_size = (self.size + 1) * self.cell_size + 2 * self.padding
        self.setFixedSize(total_size, total_size)
        
        self.setMouseTracking(True)
        
        self.previous_board = None  # For ko rule
        self.captured_black = 0
        self.captured_white = 0

        
        
        
    def get_neighbors(self, x, y):
        """Get valid neighboring positions"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                neighbors.append((new_x, new_y))
        return neighbors
    
    def get_group(self, x, y):
        """Find all connected stones of the same color"""
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
        """Count liberties of a group"""
        liberties = set()
        for x, y in group:
            for nx, ny in self.get_neighbors(x, y):
                if self.board[ny][nx] == 0:
                    liberties.add((nx, ny))
        return liberties
    
    def remove_group(self, group):
        """Remove a group of stones and count them"""
        count = len(group)
        for x, y in group:
            self.board[y][x] = 0
        return count
    
    def check_captures(self, x, y):
        """Check and perform captures after a stone is placed"""
        captured = 0
        opponent = 3 - self.board[y][x]
        
        # Check all neighboring groups
        for nx, ny in self.get_neighbors(x, y):
            if self.board[ny][nx] == opponent:
                group = self.get_group(nx, ny)
                if not self.get_liberties(group):
                    captured += self.remove_group(group)
        
        return captured
    
    def is_valid_move(self, x, y):
        """Check if a move is valid (including ko and suicide rules)"""
        if self.board[y][x] != 0:
            return False
            
        # Make temporary move
        self.board[y][x] = self.current_player
        
        # Check for ko rule
        if self.previous_board is not None and self.board == self.previous_board:
            self.board[y][x] = 0
            return False
            
        # Check if move creates a group with liberties
        group = self.get_group(x, y)
        has_liberties = bool(self.get_liberties(group))
        
        # If no liberties, check if it captures opponent stones
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
        pen = QPen(Qt.GlobalColor.black)
        pen.setWidth(1)
        painter.setPen(pen)

        # Draw vertical and horizontal lines
        for i in range(self.size):
            # Vertical lines
            start_x = self.padding + (i + 1) * self.cell_size
            painter.drawLine(start_x, self.padding + self.cell_size,
                           start_x, self.padding + self.size * self.cell_size)
            
            # Horizontal lines
            start_y = self.padding + (i + 1) * self.cell_size
            painter.drawLine(self.padding + self.cell_size, start_y,
                           self.padding + self.size * self.cell_size, start_y)

        # Draw star points
        if self.size == 9:
            star_points = [(2, 2), (2, 6), (4, 4), (6, 2), (6, 6)]
        else:  # 7x7
            star_points = [(2, 2), (2, 4), (3, 3), (4, 2), (4, 4)]

        for x, y in star_points:
            if self.board[y][x] == 0:
                center_x = self.padding + (x + 1) * self.cell_size
                center_y = self.padding + (y + 1) * self.cell_size
                painter.setBrush(QBrush(Qt.GlobalColor.black))
                painter.drawEllipse(center_x - 3, center_y - 3, 6, 6)

       # Draw stones
        for y in range(self.size):  # Add this line to create the y loop
            for x in range(self.size):
                if self.board[y][x] != 0:
                    center_x = self.padding + (x + 1) * self.cell_size
                    center_y = self.padding + (y + 1) * self.cell_size
                    stone_size = int(self.cell_size * 0.8)
                    half_stone = stone_size // 2
                    
                    # Create gradient for stones
                    if self.board[y][x] == 1:  # Black stone
                        gradient = QRadialGradient(
                            center_x - half_stone/3,
                            center_y - half_stone/3,
                            stone_size
                        )
                        gradient.setColorAt(0, QColor(96, 96, 96))
                        gradient.setColorAt(1, QColor(0, 0, 0))
                    else:  # White stone
                        gradient = QRadialGradient(
                            center_x - half_stone/3,
                            center_y - half_stone/3,
                            stone_size
                        )
                        gradient.setColorAt(0, QColor(255, 255, 255))
                        gradient.setColorAt(1, QColor(220, 220, 220))
                    
                    painter.setBrush(QBrush(gradient))
                    painter.setPen(Qt.PenStyle.NoPen)
                    painter.drawEllipse(center_x - half_stone, center_y - half_stone, stone_size, stone_size)


        # Draw coordinates
        painter.setPen(Qt.GlobalColor.black)
        for i in range(self.size):
            # Column coordinates (A-I or A-G)
            x = self.padding + (i + 1) * self.cell_size
            painter.drawText(x - 5, self.padding - 5, chr(65 + i))
            
            # Row coordinates (1-9 or 1-7)
            y = self.padding + (i + 1) * self.cell_size
            painter.drawText(self.padding - 15, y + 5, str(i + 1))

    def mousePressEvent(self, event):
        x = round((event.position().x() - self.padding - self.cell_size) / self.cell_size)
        y = round((event.position().y() - self.padding - self.cell_size) / self.cell_size)
        
        if 0 <= x < self.size and 0 <= y < self.size:
            if self.is_valid_move(x, y):
                self.pass_count = 0
                self.previous_board = [row[:] for row in self.board]
                self.board[y][x] = self.current_player
                
                # Emit move information
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
        """Reset the game state"""
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 1
        self.captured_black = 0
        self.captured_white = 0
        self.previous_board = None
        self.pass_count = 0
        self.update()
        self.game_reset.emit()  

    def pass_move(self):
        """Handle pass move"""
        self.pass_count += 1
        if self.pass_count >= 2:
            # Handle game end
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



    
        
        
                
                
                
    


class GoGame(QMainWindow):
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
        
        # Set up UI elements
        self._setup_ui_elements()
        
        # Connect signals
        self._connect_signals()
        
        # Initialize UI
        self.initUI()


    
        
    def update_captures(self, black_captures, white_captures):
        """Update the capture count labels"""
        self.black_captures_label.setText(f"Black Captures: {black_captures}")
        self.white_captures_label.setText(f"White Captures: {white_captures}")

    def create_info_panel(self):
        # Widen the info panel
        info_panel = QWidget()
        info_panel.setMinimumWidth(300)  # Increase from current narrow width
        
        # Add more information in the wider space:
        layout = QVBoxLayout()
        layout.addWidget(self.player_info)
        layout.addWidget(self.capture_info)
        layout.addWidget(self.move_history)  # New component
        layout.addWidget(self.game_controls)  # New component


    def update_current_player(self, player):
        """Update the current player label based on the player number"""
        if player == 1:  # Black's turn
            self.current_player_label.setText("Current Player: Black (○)")
            self.current_player_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    background-color: #34495e;
                    border-radius: 10px;
                    margin: 5px;
                }
            """)
        else:  # White's turn
            self.current_player_label.setText("Current Player: White (●)")
            self.current_player_label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 18px;
                    font-weight: bold;
                    padding: 10px;
                    background-color: #34495e;
                    border-radius: 10px;
                    margin: 5px;
                }
            """)

    def paintStone(self, painter, row, col, color):
        x = col * self.cell_size + self.padding
        y = row * self.cell_size + self.padding
        
        # Increase the stone size by adjusting the radius
        # The original radius is usually self.cell_size / 2 - 2
        # Let's make it bigger by using a larger fraction of the cell size
        radius = int(self.cell_size * 0.5)  # Increased from about 0.4 to 0.45
        
        # Create the stone
        stone = QRect(
            x - radius,
            y - radius,
            radius * 2,
            radius * 2
        )
        
        # Set up the gradients and colors for the stones
        if color == 'black':
            gradient = QRadialGradient(
                x - radius/3,
                y - radius/3,
                radius * 2
            )
            gradient.setColorAt(0, QColor(96, 96, 96))
            gradient.setColorAt(1, QColor(0, 0, 0))
        else:  # white
            gradient = QRadialGradient(
                x - radius/3,
                y - radius/3,
                radius * 2
            )
            gradient.setColorAt(0, QColor(255, 255, 255))
            gradient.setColorAt(1, QColor(220, 220, 220))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(stone)
        
        
    def record_move(self, x, y, player):
        """Record a move in the move history"""
        # Convert coordinates to Go notation (A-T for columns, 1-19 for rows)
        col = chr(65 + x)  # A, B, C, etc.
        row = str(y + 1)
        color = "Black" if player == 1 else "White"
        
        # Format the move entry
        move_text = f"Move {self.move_counter}: {color} - {col}{row}"
        
        # Add to list widget
        item = QListWidgetItem(move_text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        self.move_history_widget.addItem(item)
        
        # Scroll to the latest move
        self.move_history_widget.scrollToBottom()
        
        # Increment move counter
        self.move_counter += 1


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
        left_container = QVBoxLayout()
        left_container.setSpacing(20)
        
        # Info panel setup
        info_panel = QFrame()
        info_panel.setFixedWidth(300)
        info_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                        stop:0 #2c3e50, stop:1 #3498db);
                border-radius: 20px;
                padding: 20px;
            }
        """)
        
        # Info panel layout
        info_layout = QVBoxLayout(info_panel)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        info_layout.setSpacing(20)
        
        # Player information
        if self.player1 and self.player2:
            # Player 1 info
            p1_group = QGroupBox(f"Player 1: {self.player1['name']}")
            p1_layout = QVBoxLayout()
            p1_color_label = QLabel(f"Color: {self.player1['color']}")
            p1_layout.addWidget(p1_color_label)
            p1_group.setLayout(p1_layout)
            
            # Player 2 info
            p2_group = QGroupBox(f"Player 2: {self.player2['name']}")
            p2_layout = QVBoxLayout()
            p2_color_label = QLabel(f"Color: {self.player2['color']}")
            p2_layout.addWidget(p2_color_label)
            p2_group.setLayout(p2_layout)
            
            info_layout.addWidget(p1_group)
            info_layout.addWidget(p2_group)
        
        # Game status information
        info_layout.addWidget(self.current_player_label)
        info_layout.addWidget(self.black_captures_label)
        info_layout.addWidget(self.white_captures_label)
        
        # Move history
        info_layout.addWidget(self.move_history_label)
        info_layout.addWidget(self.move_history_widget)
        info_layout.addStretch()
        
        # Button frame
        button_frame = QFrame()
        button_frame.setFixedHeight(160)
        button_frame.setFixedWidth(300)
        button_frame.setStyleSheet("""
            QFrame {
                background-color: #2c2c2c;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        
        # Button layout
        button_layout = QVBoxLayout(button_frame)
        button_layout.setSpacing(10)
        
        # Button container
        top_button_container = QHBoxLayout()
        top_button_container.setSpacing(10)
        top_button_container.addWidget(self.Pass_button)
        top_button_container.addWidget(self.Reset_button)

        # Middle button container
        middle_button_container = QHBoxLayout()
        middle_button_container.setSpacing(10)
        middle_button_container.addWidget(self.pause_button)
        middle_button_container.addWidget(self.back_home_button)
        
        
        
        button_layout.addLayout(top_button_container)
        button_layout.addWidget(self.pause_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add panels to left container
        left_container.addWidget(info_panel)
        left_container.addWidget(button_frame)
        
        # Right container with board
        right_container = QFrame()
        right_container.setStyleSheet("""
            QFrame {
                background-color: #2c2c2c;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        
        # Add shadow to board container
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        right_container.setGraphicsEffect(shadow)
        
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(30, 30, 30, 30)
        
        # Configure board size
        self.board.cell_size = 80
        self.board.padding = 50
        total_size = (self.board.size + 1) * self.board.cell_size + 2 * self.board.padding
        self.board.setFixedSize(total_size, total_size)
        
        right_layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add containers to main layout
        main_layout.addLayout(left_container)
        main_layout.addWidget(right_container, 1)
        
        # Add escape key shortcut
        shortcut = QShortcut(QKeySequence('Esc'), self)
        shortcut.activated.connect(self.showNormal)




    



    def show_pause_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Game Paused")
        dialog.setFixedSize(400, 300)  # Made bigger to accommodate more buttons
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        dialog.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        message = QLabel("Game Paused")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        
        # Button style
        button_style = """
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
        """
        
        # Resume button
        resume_btn = QPushButton("Resume Game")
        resume_btn.clicked.connect(dialog.accept)
        resume_btn.setStyleSheet(button_style)
        
        # Back to home button
        back_home_btn = QPushButton("Back to Home")
        back_home_btn.setStyleSheet(button_style.replace("#3498db", "#e74c3c").replace("#2980b9", "#c0392b"))
        back_home_btn.clicked.connect(self.go_back_to_home)
        back_home_btn.clicked.connect(dialog.accept)
        
        # Container for buttons
        button_container = QVBoxLayout()
        button_container.setSpacing(15)
        button_container.addWidget(resume_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        button_container.addWidget(back_home_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
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







    def reset_game(self):
        self.move_counter = 1
        self.move_history_widget.clear()
        self.board.reset_game()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        super().keyPressEvent(event)


    def closeEvent(self, event):
        # Clean up resources
        self.board.deleteLater()
        super().closeEvent(event)


    def setup_game(self, game_settings):
        """Set up the game with the provided settings."""
        self.game_settings = game_settings
        self.player1 = game_settings['player1']
        self.player2 = game_settings['player2']
        self.game_mode = game_settings['mode']

        # Initialize the game board
        self.init_game_board()

        # Update UI with player names and colors
        self.update_player_info()

        # Start the game
        self.start_game()
        
        self.initUI()

    def init_game_board(self):
        """Initialize the game board"""
        self.board.reset_game()
        self.move_counter = 1
        self.move_history_widget.clear()

    def update_player_info(self):
        """Update the player information display."""
        if self.player1 and self.player2:
            self.current_player_label.setText(
                f"Current Player: {self.player1['name']} ({self.player1['color']})"
            )

    def start_game(self):
        """Start the game"""
        try:
            print(f"Starting game with settings: {self.game_settings}")
            self.update_player_info()
            self.board.reset_game()
        except Exception as e:
            print(f"Error in start_game: {e}")
            raise


    def _setup_ui_elements(self):
        """Set up UI elements with styles"""
        # Style for the move history widget
        self.move_history_widget.setFixedWidth(260)
        self.move_history_widget.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 5px;
                margin: 2px;
                background-color: #34495e;
                border-radius: 5px;
            }
        """)
        
        # Style for buttons
        button_style = """
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """
        
        for button in [self.Reset_button, self.Pass_button, self.pause_button]:
            button.setFixedSize(120, 40)
            button.setStyleSheet(button_style)



        self.back_home_button = QPushButton("Back to Home")
        self.back_home_button.setFixedSize(120, 40)
        self.back_home_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        

    def _connect_signals(self):
        """Connect all signals"""
        self.board.current_player_changed.connect(self.update_current_player)
        self.board.captures_changed.connect(self.update_captures)
        self.board.move_made.connect(self.record_move)
        self.Pass_button.clicked.connect(self.board.pass_move)
        self.Reset_button.clicked.connect(self.reset_game)
        self.pause_button.clicked.connect(self.show_pause_dialog)
        self.back_home_button.clicked.connect(self.go_back_to_home)



    def go_back_to_home(self):
        """Handle returning to home page with a custom QDialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirm Exit")
        dialog.setFixedSize(400, 250)
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        dialog.setGraphicsEffect(shadow)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Warning icon
        icon_label = QLabel()
        warning_icon = QApplication.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
        icon_label.setPixmap(warning_icon.pixmap(64, 64))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Message
        message = QLabel("Are you sure you want to return to the home page?")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setWordWrap(True)
        message.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        sub_message = QLabel("Current game progress will be lost.")
        sub_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sub_message.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                font-size: 14px;
            }
        """)
        
        # Button container
        button_container = QHBoxLayout()
        button_container.setSpacing(15)
        
        # Button style
        button_style = """
            QPushButton {
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: %s;
            }
        """
        
        # Yes button (red)
        yes_btn = QPushButton("Yes, Exit")
        yes_btn.setStyleSheet(button_style % "#c0392b" + """
            QPushButton {
                background-color: #e74c3c;
            }
        """)
        yes_btn.clicked.connect(lambda: self.return_to_main_page(dialog))
        
        # No button (blue)
        no_btn = QPushButton("No, Stay")
        no_btn.setStyleSheet(button_style % "#2980b9" + """
            QPushButton {
                background-color: #3498db;
            }
        """)
        no_btn.clicked.connect(dialog.reject)
        
        # Add buttons to container
        button_container.addWidget(no_btn)
        button_container.addWidget(yes_btn)
        
        # Add all elements to main layout
        layout.addStretch()
        layout.addWidget(icon_label)
        layout.addWidget(message)
        layout.addWidget(sub_message)
        layout.addSpacing(20)
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


    def return_to_main_page(self, dialog):
        """Switch back to the main menu and close the dialog."""
        self.close  # Switch to the main menu


    



   






    

