from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class EndGameOverlay(QWidget):
    def __init__(self, winner=None, final_score=None, move_history=None, parent=None, board_state=None):
        super().__init__(parent)
        self.parent = parent
        
        # If board_state is provided, calculate winner and score
        if board_state is not None:
            self.board_state = board_state
            winner, final_score = self.determine_winner()
        else:
            # Use provided winner and score
            self.winner = winner
            self.final_score = final_score if final_score else {'black': 0, 'white': 0}
            
        self.init_ui(winner, self.final_score)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def determine_winner(self):
        """
        Determines the winner based on the final board state and scoring rules.
        Returns tuple of (winner_text, score_dict)
        """
        black_score = 0
        white_score = 0
        board_size = len(self.board_state)
        
        # Count stones and territory
        for row in range(board_size):
            for col in range(board_size):
                current = self.board_state[row][col]
                if current == 'B':
                    black_score += 1
                elif current == 'W':
                    white_score += 1
        
        # Add territory points (empty intersections surrounded by stones)
        territory_points = self.calculate_territory()
        black_score += territory_points['black']
        white_score += territory_points['white']
        
        # Determine winner
        if black_score > white_score:
            winner = "Black"
        elif white_score > black_score:
            winner = "White"
        else:
            winner = "Draw"
            
        return winner, {'black': black_score, 'white': white_score}
    
    def calculate_territory(self):
        """
        Calculates territory points for both players.
        Returns dict with territory points for each color.
        """
        territory = {'black': 0, 'white': 0}
        board_size = len(self.board_state)
        visited = [[False] * board_size for _ in range(board_size)]
        
        def flood_fill(row, col, visited):
            if (row < 0 or row >= board_size or 
                col < 0 or col >= board_size or 
                visited[row][col] or 
                self.board_state[row][col] != '.'):
                return None, set()
            
            territory_points = set()
            surrounding_colors = set()
            stack = [(row, col)]
            
            while stack:
                current_row, current_col = stack.pop()
                if visited[current_row][current_col]:
                    continue
                    
                visited[current_row][current_col] = True
                territory_points.add((current_row, current_col))
                
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    next_row, next_col = current_row + dr, current_col + dc
                    if 0 <= next_row < board_size and 0 <= next_col < board_size:
                        if self.board_state[next_row][next_col] in ['B', 'W']:
                            surrounding_colors.add(self.board_state[next_row][next_col])
                        elif not visited[next_row][next_col]:
                            stack.append((next_row, next_col))
            
            if len(surrounding_colors) == 1:
                return list(surrounding_colors)[0], territory_points
            return None, set()
        
        for row in range(board_size):
            for col in range(board_size):
                if not visited[row][col] and self.board_state[row][col] == '.':
                    owner, territory_points = flood_fill(row, col, visited)
                    if owner == 'B':
                        territory['black'] += len(territory_points)
                    elif owner == 'W':
                        territory['white'] += len(territory_points)
        
        return territory

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
        trophy_label = QLabel("🏆" if winner != "Draw" else "🤝")
        trophy_label.setFont(QFont('Segoe UI', 48))
        trophy_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        trophy_label.setStyleSheet("color: white; border: none;")
        
        winner_text = QLabel(f"{winner} Wins!" if winner != "Draw" else "It's a Draw!")
        winner_text.setFont(QFont('Segoe UI', 36, QFont.Weight.Bold))
        winner_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        winner_text.setStyleSheet("color: white; border: none;")
        
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setOffset(0, 0)
        glow.setColor(QColor('#3498db'))
        winner_text.setGraphicsEffect(glow)
        
        score_text = QLabel(
            f"Final Score\n"
            f"Black: {final_score['black']} points\n"
            f"White: {final_score['white']} points"
        )
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
        
        layout.addWidget(content_container)
        layout.addWidget(button_container)


# Add this new class for detection popups
class DetectionPopup(QWidget):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui(message)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def init_ui(self, message):
        self.setFixedSize(500, 300)  # Smaller size for popup
        
        if self.parent:
            parent_geometry = self.parent.geometry()
            x = parent_geometry.center().x() - self.width() // 2
            y = parent_geometry.center().y() - self.height() // 2
            self.move(x, y)
        
        # Main container frame
        main_frame = QFrame(self)
        main_frame.setObjectName("mainFrame")
        main_frame.setGeometry(0, 0, 500, 300)
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
        
        # Alert icon
        alert_label = QLabel("⚠️")  # Alert emoji
        alert_label.setFont(QFont('Segoe UI', 48))
        alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        alert_label.setStyleSheet("color: white; border: none;")
        
        # Message text
        message_text = QLabel(message)
        message_text.setFont(QFont('Segoe UI', 24, QFont.Weight.Bold))
        message_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_text.setStyleSheet("color: white; border: none;")
        message_text.setWordWrap(True)
        
        # Add glow effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setOffset(0, 0)
        glow.setColor(QColor('#3498db'))
        message_text.setGraphicsEffect(glow)
        
        content_layout.addWidget(alert_label)
        content_layout.addWidget(message_text)
        
        # Buttons
        button_container = QFrame()
        button_container.setStyleSheet("background: transparent; border: none;")
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)
        
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
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setStyleSheet(button_style)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.ok_btn.setGraphicsEffect(shadow)
        self.ok_btn.setFixedWidth(200)
        self.ok_btn.clicked.connect(self.close)
        
        button_layout.addWidget(self.ok_btn)
        
        layout.addWidget(content_container)
        layout.addWidget(button_container)

# Usage example in your board class:
    def show_detection_popup(self, message):
        self.detection_popup = DetectionPopup(message, self)
        self.detection_popup.show()