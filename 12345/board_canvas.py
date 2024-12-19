from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
import styles

class BoardCanvas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.go_board = parent
        
        # Get screen size
        screen = self.screen()
        screen_size = screen.size()
        
        # Set minimum size based on screen dimensions
        min_dimension = min(screen_size.width(), screen_size.height())
        # Convert float to int for QSize
        min_size = int(min_dimension * 0.6)
        self.setMinimumSize(QSize(min_size, min_size))
        
        self.setMouseTracking(True)
        self.hover_pos = None
        self.col_coords = []
        self.row_coords = []
        self.cell_size = 0
        self.start_x = 0
        self.start_y = 0
        self.update_coordinates()

    def update_coordinates(self):
        """Update coordinates based on current board size"""
        self.col_coords = [chr(i) for i in range(65, 65 + self.go_board.board_size)]
        self.row_coords = [str(i) for i in range(1, self.go_board.board_size + 1)]
        self.cell_size = min(self.width(), self.height()) // (self.go_board.board_size + 1)
        self.update()  # Force a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Calculate board dimensions
        total_board_size = self.cell_size * (self.go_board.board_size - 1)
        self.start_x = (self.width() - total_board_size) // 2
        self.start_y = (self.height() - total_board_size) // 2

        # Draw board background
        painter.fillRect(self.rect(), QColor('#DCB35C'))

        # Set up pen for grid lines
        painter.setPen(QPen(QColor(styles.COLORS['board_lines']), 1))

        # Draw the board elements in order
        self._draw_coordinates(painter, self.start_x, self.start_y, self.cell_size, total_board_size)
        self._draw_grid_lines(painter, self.start_x, self.start_y, total_board_size)
        self._draw_star_points(painter, self.start_x, self.start_y, self.cell_size)
        
        # Draw territory markers if game has ended
        if self.go_board.game_ended:
            self._draw_territory_markers(painter, self.start_x, self.start_y, self.cell_size)
        
        # Draw stones
        self._draw_stones(painter, self.start_x, self.start_y, self.cell_size)
        
        # Draw hover stone (only if game is not ended)
        if not self.go_board.game_ended:
            self._draw_hover_stone(painter, self.start_x, self.start_y, self.cell_size)

    def _draw_coordinates(self, painter, start_x, start_y, cell_size, total_board_size):
        painter.setPen(QPen(QColor('#000000')))
        font = painter.font()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)

        for i in range(self.go_board.board_size):
            x = start_x + i * cell_size
            y = start_y + i * cell_size

            # Draw column coordinates (A, B, C, ...)
            painter.drawText(x - 10, start_y - 20, 20, 20,
                           Qt.AlignmentFlag.AlignCenter, self.col_coords[i])
            painter.drawText(x - 10, start_y + total_board_size + 5, 20, 20,
                           Qt.AlignmentFlag.AlignCenter, self.col_coords[i])

            # Draw row coordinates (1, 2, 3, ...)
            painter.drawText(start_x - 30, y - 10, 20, 20,
                           Qt.AlignmentFlag.AlignCenter, self.row_coords[i])
            painter.drawText(start_x + total_board_size + 10, y - 10, 20, 20,
                           Qt.AlignmentFlag.AlignCenter, self.row_coords[i])

    def _draw_grid_lines(self, painter, start_x, start_y, total_board_size):
        for i in range(self.go_board.board_size):
            # Draw horizontal lines
            painter.drawLine(
                start_x, start_y + i * self.cell_size,
                start_x + total_board_size, start_y + i * self.cell_size
            )
            # Draw vertical lines
            painter.drawLine(
                start_x + i * self.cell_size, start_y,
                start_x + i * self.cell_size, start_y + total_board_size
            )

    def _draw_star_points(self, painter, start_x, start_y, cell_size):
        if self.go_board.board_size == 9:
            star_points = [(2, 2), (2, 6), (4, 4), (6, 2), (6, 6)]
        elif self.go_board.board_size == 7:
            star_points = [(3, 3)]
        else:
            return

        painter.setBrush(QBrush(QColor(styles.COLORS['board_lines'])))
        for x, y in star_points:
            center_x = int(start_x + x * cell_size)
            center_y = int(start_y + y * cell_size)
            painter.drawEllipse(center_x - 3, center_y - 3, 6, 6)

    def _draw_stones(self, painter, start_x, start_y, cell_size):
        for row in range(self.go_board.board_size):
            for col in range(self.go_board.board_size):
                if self.go_board.board_state[row][col]:
                    color = QColor('black') if self.go_board.board_state[row][col] == 'black' else QColor('white')
                    painter.setBrush(QBrush(color))
                    painter.setPen(Qt.PenStyle.NoPen if self.go_board.board_state[row][col] == 'black' 
                                 else QPen(QColor('black')))
                    
                    center_x = int(start_x + col * cell_size)
                    center_y = int(start_y + row * cell_size)
                    center = QPoint(center_x, center_y)
                    
                    stone_radius = int(cell_size * 0.45)
                    painter.drawEllipse(center, stone_radius, stone_radius)

    def _draw_hover_stone(self, painter, start_x, start_y, cell_size):
        if self.hover_pos:
            x, y = self.hover_pos
            center_x = int(start_x + x * cell_size)
            center_y = int(start_y + y * cell_size)
            stone_radius = int(cell_size * 0.45)

            shadow_color = QColor('black' if self.go_board.current_player == 'black' else 'white')
            shadow_color.setAlpha(128)

            painter.setBrush(QBrush(shadow_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QPoint(center_x, center_y), stone_radius, stone_radius)

    def _draw_territory_markers(self, painter, start_x, start_y, cell_size):
        if self.go_board.game_ended:
            for row in range(self.go_board.board_size):
                for col in range(self.go_board.board_size):
                    if self.go_board.territory[row][col]:
                        center_x = int(start_x + col * cell_size)
                        center_y = int(start_y + row * cell_size)
                        color = QColor('#3498db' if self.go_board.territory[row][col] == 'black' else '#e74c3c')
                        color.setAlpha(100)
                        painter.setBrush(QBrush(color))
                        painter.setPen(Qt.PenStyle.NoPen)
                        painter.drawRect(
                            center_x - cell_size//2,
                            center_y - cell_size//2,
                            cell_size,
                            cell_size
                        )

    def mouseMoveEvent(self, event):
        x = round((event.position().x() - self.start_x) / self.cell_size)
        y = round((event.position().y() - self.start_y) / self.cell_size)

        if (0 <= x < self.go_board.board_size and 
            0 <= y < self.go_board.board_size and 
            self.go_board.board_state[y][x] is None):  # Add check for empty position
            self.hover_pos = (x, y)
        else:
            self.hover_pos = None

        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x = round((event.position().x() - self.start_x) / self.cell_size)
            y = round((event.position().y() - self.start_y) / self.cell_size)
            
            if (0 <= x < self.go_board.board_size and 
                0 <= y < self.go_board.board_size):
                
                try:
                    # Add check for correct player's turn
                    if self.go_board.is_valid_move(x, y):
                        success = self.go_board.make_move(x, y)
                        if success:
                            self.update()
                        else:
                            print("Invalid move: Move was not successful")
                except Exception as e:
                    print(f"Error placing stone: {e}")

    def leaveEvent(self, event):
        self.hover_pos = None
        self.update()