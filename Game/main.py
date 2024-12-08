import sys

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class MainGame(QWidget):

    current_player_changed = pyqtSignal(int)
    captures_changed = pyqtSignal(int, int)  # Move this to class level
    move_made = pyqtSignal(int, int, int)  # Add new signal (x, y, player)


    def __init__(self, size=9):
        super().__init__()
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]
        self.cell_size = 40
        self.padding = 20
        self.current_player = 1

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
                
                
                
    


class GoGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1200, 800)  # Instead of current smaller size
        
        # Adjust layout proportions
        self.main_layout = QHBoxLayout()
        self.main_layout.setStretch(0, 1)  # Info panel
        self.main_layout.setStretch(1, 3) 
        # Create the game board and labels with styled appearance
        self.board = MainGame(9)

        # Connect the signal to update the label
        self.board.current_player_changed.connect(self.update_current_player)
        
        # Style the labels with custom font and colors
        self.current_player_label = QLabel("Current Player: Black (○)")
        self.black_captures_label = QLabel("Black Captures: 0")
        self.white_captures_label = QLabel("White Captures: 0")
        
        # Create move history list widget
        self.move_history_widget = QListWidget()
        self.move_history_widget.setFixedWidth(260)  # Match info panel width
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
            QListWidget::item:hover {
                background-color: #3498db;
            }
            QScrollBar:vertical {
                border: none;
                background: #2c3e50;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # Add move history label
        self.move_history_label = QLabel("Move History")
        self.move_history_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
        """)

        # Connect the move signal
        self.board.move_made.connect(self.record_move)
        
        # Move counter
        self.move_counter = 1
        
        # Create a styled pause button
        self.pause_button = QPushButton("Pause")
        self.pause_button.setFixedSize(120, 40)
        self.pause_button.setStyleSheet("""
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
            QPushButton:pressed {
                background-color: #2980b9;
            }
        """)
        
        # Apply styles to labels
        label_style = """
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #34495e;
                border-radius: 10px;
                margin: 5px;
            }
        """
        self.current_player_label.setStyleSheet(label_style)
        self.black_captures_label.setStyleSheet(label_style)
        self.white_captures_label.setStyleSheet(label_style)
        
        # Connect captures signal
        self.board.captures_changed.connect(self.update_captures)
        
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

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Left side container
        left_container = QVBoxLayout()
        left_container.setSpacing(20)
        
        # Left info panel with gradient background
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
        
        info_layout = QVBoxLayout(info_panel)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        info_layout.setSpacing(20)
        
        # Add game info widgets to info panel
        info_layout.addWidget(self.current_player_label)
        info_layout.addWidget(self.black_captures_label)
        info_layout.addWidget(self.white_captures_label)
        info_layout.addStretch()
        
         # Add move history to info panel
        info_layout.addWidget(self.move_history_label)
        info_layout.addWidget(self.move_history_widget)
        
        # Add some spacing before the pause button
        info_layout.addSpacing(20)
        
        # Add pause button frame under info panel
        pause_frame = QFrame()
        pause_frame.setFixedHeight(80)
        pause_frame.setFixedWidth(300)
        pause_frame.setStyleSheet("""
            QFrame {
                background-color: #2c2c2c;
                border-radius: 15px;
            }
        """)
        pause_layout = QHBoxLayout(pause_frame)
        pause_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pause_layout.addWidget(self.pause_button)
        
        # Add info panel and pause button to left container
        left_container.addWidget(info_panel)
        left_container.addWidget(pause_frame)
        
        # Right container with board
        right_container = QFrame()
        right_container.setStyleSheet("""
            QFrame {
                background-color: #2c2c2c;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        
        # Add shadow effect to board container
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 0)
        right_container.setGraphicsEffect(shadow)
        
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(30, 30, 30, 30)
        
        # Make the board bigger
        self.board.cell_size = 80  # Increase cell size
        self.board.padding = 50    # Increase padding
        total_size = (self.board.size + 1) * self.board.cell_size + 2 * self.board.padding
        self.board.setFixedSize(total_size, total_size)
        
        right_layout.addWidget(self.board, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add containers to main layout
        main_layout.addLayout(left_container)
        main_layout.addWidget(right_container, 1)
        
        # Add escape key shortcut
        shortcut = QShortcut(QKeySequence('Esc'), self)
        shortcut.activated.connect(self.showNormal)




    

