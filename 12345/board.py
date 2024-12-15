from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QFrame, QGridLayout, QListWidget, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from board_canvas import BoardCanvas
from PyQt6.QtCore import QTimer

class GoBoard(QWidget):
    def __init__(self, size=9):
        super().__init__()
        # Initialize variables
        self.player1_name = ""
        self.player2_name = ""
        self.current_player = 'black'
        self.board_size = size
        
        # Get screen size
        screen = self.screen()
        self.screen_width = screen.size().width()
        self.screen_height = screen.size().height()
        
        # Adjust cell size based on screen size (ensure integer values)
        self.cell_size = int(min(self.screen_width, self.screen_height) // (size + 2))
        self.board_margin = self.cell_size
        
        # Timer initialization
        self.timer = QTimer()
        self.black_time = 30 * 60
        self.white_time = 30 * 60
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        
        # Other initializations
        self.captured_black = 0
        self.captured_white = 0
        self.move_history = []
        self.game_ended = False
        self.territory_score = {'black': 0, 'white': 0}
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        # Initialize board state and territory
        self.board_state = [[None for _ in range(size)] for _ in range(size)]
        self.territory = [[None for _ in range(size)] for _ in range(size)]
        
        # Create UI
        self.init_ui()
        self.setup_connections()
        
        # Set window to fullscreen
        self.showFullScreen()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(int(self.screen_height * 0.02))
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        game_content = QHBoxLayout()
        game_content.setSpacing(int(self.screen_width * 0.02))
        
        left_panel = self.create_left_panel()
        game_content.addWidget(left_panel)
        
        board_container = self.create_board_container()
        game_content.addWidget(board_container, 1)
        
        button_container = self.create_button_container()
        
        main_layout.addLayout(game_content)
        main_layout.addWidget(button_container)
        
        self.setLayout(main_layout)


    def create_left_panel(self):
        panel = QFrame()
        panel.setObjectName("leftPanel")
        
        # Calculate panel width based on screen size (ensure integer)
        panel_width = int(self.screen_width * 0.2)  # 20% of screen width
        panel.setFixedWidth(panel_width)
    
    
  
        panel.setStyleSheet("""
            QFrame#leftPanel {
                background-color: #2C3E50;
                border-radius: 15px;
                padding: 15px;
            }
            QLabel {
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 8px;
            }
            QListWidget {
                background-color: rgba(52, 73, 94, 0.7);
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 8px;
                margin: 3px 0px;
                background-color: rgba(44, 62, 80, 0.6);
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: rgba(44, 62, 80, 0.8);
            }
        """)
        panel.setFixedWidth(300)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Current Player Section
        current_player_frame = QFrame()
        current_player_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(41, 128, 185, 0.7);
                border-radius: 8px;
                padding: 5px;
            }
        """)
        self.current_player_label = QLabel()
        self.current_player_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """)
        current_player_layout = QVBoxLayout(current_player_frame)
        current_player_layout.addWidget(self.current_player_label)

        # Player Info Section
        player_info_frame = QFrame()
        player_info_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(52, 73, 94, 0.7);
                border-radius: 8px;
                padding: 6px;
            }
        """)
        player_info_layout = QVBoxLayout(player_info_frame)
        
        # Black Player Info
        black_section = QFrame()
        black_section.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.3);
                border-radius: 6px;
                margin: 2px;
            }
        """)
        black_layout = QVBoxLayout(black_section)
        self.player1_name_label = QLabel()
        self.player1_captures_label = QLabel()
        black_layout.addWidget(self.player1_name_label)
        black_layout.addWidget(self.player1_captures_label)

        # In the black player section (black_layout)
        self.black_timer_label = QLabel()
        self.black_timer_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background: transparent;
            }
        """)
        black_layout.addWidget(self.black_timer_label)
        
        # White Player Info
        white_section = QFrame()
        white_section.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                margin: 2px;
            }
        """)
        white_layout = QVBoxLayout(white_section)
        self.player2_name_label = QLabel()
        self.player2_captures_label = QLabel()
        white_layout.addWidget(self.player2_name_label)
        white_layout.addWidget(self.player2_captures_label)

        self.white_timer_label = QLabel()
        self.white_timer_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background: transparent;
            }
        """)
        white_layout.addWidget(self.white_timer_label)
        
        player_info_layout.addWidget(black_section)
        player_info_layout.addWidget(white_section)
        
        # Move History Section
        history_frame = QFrame()
        history_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(52, 73, 94, 0.7);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        history_layout = QVBoxLayout(history_frame)
        
        history_label = QLabel("Move History")
        history_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """)
        
        self.history_list = QListWidget()
        self.history_list.setMinimumHeight(300)
        
        history_layout.addWidget(history_label)
        history_layout.addWidget(self.history_list)
        
        # Add all sections to main layout
        layout.addWidget(current_player_frame)
        layout.addWidget(player_info_frame)
        layout.addWidget(history_frame)
        
        return panel

    def create_board_container(self):
        try:
            container = QFrame()
            container.setObjectName("boardContainer")
            container.setStyleSheet("""
                QFrame#boardContainer {
                    background-color: #34495E;
                    border-radius: 15px;
                    padding: 15px;
                }
            """)
            
            layout = QVBoxLayout(container)
            self.board_canvas = BoardCanvas(self)
            layout.addWidget(self.board_canvas)
            
            return container
        except Exception as e:
            print(f"Error creating board container: {e}")
            import traceback
            traceback.print_exc()
            raise


    def make_move(self, x, y):
        """Handle making a move"""
        try:
            # Check if it's the correct player's turn
            if self.move_history and self.move_history[-1].startswith('●' if self.current_player == 'black' else '○'):
                return False
            
            self.board_state[y][x] = self.current_player
            
            # Process captures
            captures = self.check_captures(x, y)
            
            # Check if move is still valid after captures
            if not captures and self.get_liberties(x, y) == 0:
                self.board_state[y][x] = None
                return False
            
            # Get current player name and symbol
            current_name = (self.player1_name if self.current_player == 'black' 
                        else self.player2_name)
            symbol = '●' if self.current_player == 'black' else '○'
            
            # Convert numeric column to letter (0=A, 1=B, etc.)
            col_letter = chr(65 + x)
            
            # Add move to history
            move_text = f"{symbol} {current_name}: {col_letter}{y+1}"
            self.move_history.append(move_text)
            
            # Switch player and update UI
            self.switch_player()
            self.update_history()
            self.update_labels()
            self.update_board()  # Add this line
            
            return True
            
        except Exception as e:
            print(f"Error in make_move: {e}")
            self.board_state[y][x] = None
            return False

    def create_button_container(self):
        container = QFrame()
        container.setObjectName("buttonContainer")
        
        # Calculate button sizes based on screen size (ensure integer)
        button_height = int(self.screen_height * 0.06)
        
        container.setStyleSheet(f"""
            QFrame#buttonContainer {{
                background-color: #34495E;
                border-radius: 15px;
                padding: 15px;
                margin: 10px;
                min-height: {button_height}px;
            }}
        """)
        
        layout = QHBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # Create buttons with icons
        self.back_btn = QPushButton("← Back to Menu")
        self.reset_btn = QPushButton("↺ Reset Game")
        self.pass_btn = QPushButton("⟳ Pass Turn")
        
        # Style buttons
        button_style = """
            QPushButton {
                background-color: %s;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: %s;
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background-color: %s;
                transform: translateY(1px);
            }
        """
        
        # Back button (Red)
        self.back_btn.setStyleSheet(button_style % ('#E74C3C', '#C0392B', '#922B21'))
        
        # Reset button (Orange)
        self.reset_btn.setStyleSheet(button_style % ('#F39C12', '#D35400', '#A04000'))
        
        # Pass button (Blue)
        self.pass_btn.setStyleSheet(button_style % ('#3498DB', '#2980B9', '#1F618D'))
        
        # Add shadow effect to buttons
        for btn in [self.back_btn, self.reset_btn, self.pass_btn]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setOffset(0, 3)
            shadow.setColor(QColor(0, 0, 0, 60))
            btn.setGraphicsEffect(shadow)
        
        # Add buttons to layout
        layout.addWidget(self.back_btn)
        layout.addWidget(self.reset_btn)
        layout.addWidget(self.pass_btn)
        
        return container

    def update_labels(self):
        """Update UI labels"""
        try:
            # Update current player
            current_name = self.player1_name if self.current_player == "black" else self.player2_name
            self.current_player_label.setText(f"Current Player: {current_name}")
            
            # Update player info
            self.player1_name_label.setText(f"● Black: {self.player1_name}")
            self.player2_name_label.setText(f"○ White: {self.player2_name}")
            self.player1_captures_label.setText(f"Captures: {self.captured_black}")
            self.player2_captures_label.setText(f"Captures: {self.captured_white}")
        except Exception as e:
            print(f"Error updating labels: {e}")

    def set_player_info(self, player1_name, player2_name):
        """Set player information"""
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.update_labels()

    def get_liberties(self, x, y, visited=None):
        """Count liberties of a stone or group"""
        if visited is None:
            visited = set()
                
        color = self.board_state[y][x]
        if color is None:
            return 0
                
        visited.add((x, y))
        liberties = set()
            
        for dx, dy in self.directions:
            new_x, new_y = x + dx, y + dy
                
            if not (0 <= new_x < self.board_size and 0 <= new_y < self.board_size):
                continue
                    
            if self.board_state[new_y][new_x] is None:
                liberties.add((new_x, new_y))
            elif (self.board_state[new_y][new_x] == color and 
                (new_x, new_y) not in visited):
                # Fix: Don't try to update with an integer
                group_liberties = self.get_liberties(new_x, new_y, visited)
                if isinstance(group_liberties, set):
                    liberties.update(group_liberties)
                else:
                    liberties.add((new_x, new_y))
                        
        return liberties  # Return the set of liberty positions

    def find_group(self, x, y, visited=None):
        """Find all connected stones of the same color"""
        if visited is None:
            visited = set()
            
        color = self.board_state[y][x]
        if color is None:
            return set()
            
        group = {(x, y)}
        visited.add((x, y))
        
        for dx, dy in self.directions:
            new_x, new_y = x + dx, y + dy
            
            if (0 <= new_x < self.board_size and 
                0 <= new_y < self.board_size and 
                self.board_state[new_y][new_x] == color and 
                (new_x, new_y) not in visited):
                group.update(self.find_group(new_x, new_y, visited))
                
        return group

    def check_captures(self, x, y):
        """Check and remove captured stones"""
        captured = 0
        opponent = 'white' if self.current_player == 'black' else 'black'
        
        for dx, dy in self.directions:
            new_x, new_y = x + dx, y + dy
            
            if not (0 <= new_x < self.board_size and 0 <= new_y < self.board_size):
                continue
                
            if self.board_state[new_y][new_x] == opponent:
                group = self.find_group(new_x, new_y)
                has_liberties = False
                
                for gx, gy in group:
                    liberties = self.get_liberties(gx, gy)
                    if isinstance(liberties, set):
                        has_liberties = len(liberties) > 0
                    else:
                        has_liberties = liberties > 0
                    if has_liberties:
                        break
                
                if not has_liberties:
                    for gx, gy in group:
                        self.board_state[gy][gx] = None
                    captured += len(group)
                    
                    if self.current_player == 'black':
                        self.captured_black += len(group)
                    else:
                        self.captured_white += len(group)
        
        return captured > 0

    def is_valid_move(self, x, y):
        """Check if a move is valid"""
        if not (0 <= x < self.board_size and 0 <= y < self.board_size):
            return False
                
        if self.board_state[y][x] is not None:
            return False
                
        self.board_state[y][x] = self.current_player
        captured = self.check_captures(x, y)
        liberties = self.get_liberties(x, y)
        has_liberties = len(liberties) > 0 if isinstance(liberties, set) else liberties > 0
        
        self.board_state[y][x] = None
        return captured or has_liberties

    

    def calculate_territory(self):
        """Calculate territory ownership"""
        visited = [[False for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.territory = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.territory_score = {'black': 0, 'white': 0}

        def flood_fill(x, y):
            """Flood fill algorithm to determine territory ownership"""
            if not (0 <= x < self.board_size and 0 <= y < self.board_size):
                return set(), set()
            if visited[y][x]:
                return set(), set()
            if self.board_state[y][x] is not None:
                return set(), {self.board_state[y][x]}

            visited[y][x] = True
            empty_points = {(x, y)}
            bordering_colors = set()

            # Check all four directions
            for dx, dy in self.directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < self.board_size and 0 <= new_y < self.board_size:
                    if self.board_state[new_y][new_x] is not None:
                        # If we find a stone, add its color to bordering colors
                        bordering_colors.add(self.board_state[new_y][new_x])
                    else:
                        # If empty, continue flood fill
                        points, colors = flood_fill(new_x, new_y)
                        empty_points.update(points)
                        bordering_colors.update(colors)

            return empty_points, bordering_colors

        def is_completely_surrounded(points, color):
            """Check if a set of points is completely surrounded by one color"""
            for px, py in points:
                for dx, dy in self.directions:
                    nx, ny = px + dx, py + dy
                    if (0 <= nx < self.board_size and 
                        0 <= ny < self.board_size and 
                        self.board_state[ny][nx] is not None and 
                        self.board_state[ny][nx] != color):
                        return False
            return True

        # Find territories
        for y in range(self.board_size):
            for x in range(self.board_size):
                if not visited[y][x] and self.board_state[y][x] is None:
                    empty_points, bordering_colors = flood_fill(x, y)
                    
                    # Check if the area is completely surrounded by one color
                    if len(bordering_colors) == 1:
                        owner = bordering_colors.pop()
                        if is_completely_surrounded(empty_points, owner):
                            for px, py in empty_points:
                                self.territory[py][px] = owner
                                self.territory_score[owner] += 1
                    else:
                        # Mark as neutral territory
                        for px, py in empty_points:
                            self.territory[py][px] = None

        # Add captures to final score
        self.territory_score['black'] += self.captured_black
        self.territory_score['white'] += self.captured_white

    def end_game(self):
        """End the game and calculate final score"""
        self.timer.stop() 
        self.game_ended = True
        self.calculate_territory()
        final_score = {
            'black': self.territory_score['black'] + self.captured_black,
            'white': self.territory_score['white'] + self.captured_white
        }
        winner = 'Black' if final_score['black'] > final_score['white'] else 'White'
        self.move_history.append(f"Game Over!")
        self.move_history.append(f"Black Score: {final_score['black']}")
        self.move_history.append(f"White Score: {final_score['white']}")
        self.move_history.append(f"{winner} wins!")
        self.update_history()
        self.update()

    def setup_connections(self):
        """Set up button connections"""
        try:
            self.pass_btn.clicked.connect(self.pass_turn)
            self.reset_btn.clicked.connect(self.reset_board)
            # Don't connect back_btn here as it's handled in go_game.py
        except Exception as e:
            print(f"Error setting up connections: {e}")

    def pass_turn(self):
        """Handle pass turn action"""
        self.switch_player()
        self.move_history.append(f"{self.current_player.capitalize()} passed")
        self.update_history()
        self.update_labels()

    def resign_game(self):
        """Handle resignation"""
        winner = "White" if self.current_player == "black" else "Black"
        self.move_history.append(f"{self.current_player.capitalize()} resigned. {winner} wins!")
        self.update_history()
        # Here you could add game over logic

    def undo_move(self):
        """Handle undo move action"""
        if self.move_history:
            self.move_history.pop()
            # Here you would need to implement the actual board state reversal
            self.switch_player()
            self.update_history()
            self.update_labels()
            self.update()

    def switch_player(self):
        """Switch current player"""
        self.current_player = 'white' if self.current_player == 'black' else 'black'
        self.update_labels()

    

    def update_history(self):
        """Update move history list"""
        self.history_list.clear()
        self.history_list.addItems(self.move_history)
        self.history_list.scrollToBottom()

    # In board.py, modify the set_board_size method
    def set_board_size(self, size):
        """Change the board size and reset the game"""
        try:
            print(f"Setting board size to: {size}")  # Debug print
            if size not in [7, 9]:  # Changed from if size in [7, 9]:
                raise ValueError(f"Invalid board size: {size}. Must be 7 or 9.")
                
            self.board_size = size
            # Reinitialize board state with new size
            self.board_state = [[None for _ in range(size)] for _ in range(size)]
            self.territory = [[None for _ in range(size)] for _ in range(size)]
            
            # Adjust cell size based on board size
            self.cell_size = min(600 // (size + 1), 60)
            
            # Reset game state
            self.current_player = 'black'
            self.captured_black = 0
            self.captured_white = 0
            self.move_history.clear()
            self.game_ended = False
            
            # Update coordinates for BoardCanvas
            if hasattr(self, 'board_canvas'):
                self.board_canvas.update_coordinates()
            
            # Update UI
            if hasattr(self, 'history_list'):
                self.update_history()
            if hasattr(self, 'current_player_label'):
                self.update_labels()
            
            # Force update of the board canvas
            if hasattr(self, 'board_canvas'):
                self.board_canvas.update()
            
            self.update()
            print(f"Board size updated successfully to {size}")  # Debug print
                
        except Exception as e:
            print(f"Error in set_board_size: {e}")
            import traceback
            traceback.print_exc()


    def reset_board(self):
        """Reset the board state"""
        self.board_state = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'black'
        self.last_move = None
        self.captured_black = 0
        self.captured_white = 0
        self.move_history.clear()
        # Reset timers
        self.black_time = 30 * 60
        self.white_time = 30 * 60
        self.timer.start()
        self.update_timer_labels()
        self.update_history()
        self.update_labels()
        self.update()



    def check_game_end(self):
        """Check if the game should end"""
        if len(self.move_history) >= 2:
            if self.move_history[-1].endswith("passed") and self.move_history[-2].endswith("passed"):
                self.end_game()
                return True
        return False
    


    def update_board(self):
        """Update the board display"""
        if hasattr(self, 'board_canvas'):
            self.board_canvas.update()


    def update_timer(self):
        """Update the game timer"""
        if not self.game_ended:
            if self.current_player == 'black':
                self.black_time -= 1
            else:
                self.white_time -= 1
            
            self.update_timer_labels()
            
            # Check for time out
            if self.black_time <= 0 or self.white_time <= 0:
                self.handle_time_out()

    def update_timer_labels(self):
        """Update the timer display labels"""
        black_minutes = self.black_time // 60
        black_seconds = self.black_time % 60
        white_minutes = self.white_time // 60
        white_seconds = self.white_time % 60
        
        self.black_timer_label.setText(f"Time: {black_minutes:02d}:{black_seconds:02d}")
        self.white_timer_label.setText(f"Time: {white_minutes:02d}:{white_seconds:02d}")

    def handle_time_out(self):
        """Handle when a player runs out of time"""
        self.timer.stop()
        self.game_ended = True
        winner = "White" if self.black_time <= 0 else "Black"
        self.move_history.append(f"Time Out! {winner} wins!")
        self.update_history()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


    




    

    


         