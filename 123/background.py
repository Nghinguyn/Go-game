from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QRadialGradient
import random, math

class Stone:
    def __init__(self, x, y, is_black):
        self.pos = QPointF(x, y)
        self.is_black = is_black
        self.direction = random.uniform(0, 2 * math.pi)
        self.speed = 0.5
        
        # Movement bounds
        self.min_x = x - 20
        self.max_x = x + 20
        self.min_y = y - 20
        self.max_y = y + 20
        
        self.direction_timer = 0
        self.direction_change_interval = random.uniform(2.0, 4.0)

    def update(self, time):
        self.direction_timer += time
        if self.direction_timer >= self.direction_change_interval:
            self.direction_timer = 0
            self.direction_change_interval = random.uniform(2.0, 4.0)
            self.direction += random.uniform(-0.5, 0.5)
            
        dx = math.cos(self.direction) * self.speed
        dy = math.sin(self.direction) * self.speed
        
        new_x = self.pos.x() + dx
        new_y = self.pos.y() + dy
        
        if new_x < self.min_x or new_x > self.max_x:
            self.direction = math.pi - self.direction
        if new_y < self.min_y or new_y > self.max_y:
            self.direction = -self.direction
            
        self.pos = QPointF(
            max(self.min_x, min(self.max_x, self.pos.x() + dx)),
            max(self.min_y, min(self.max_y, self.pos.y() + dy))
        )

class BackgroundWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        
        self.stones = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(1000 // 60)  # 60 FPS
        self.time = 0.0
        self.delta_time = 1.0 / 60.0
        
        self.setMinimumSize(800, 600)
        self._initialize_stones()

    def _initialize_stones(self):
        for _ in range(20):
            x = random.randint(30, self.width() - 30)
            y = random.randint(30, self.height() - 30)
            is_black = random.choice([True, False])
            self.stones.append(Stone(x, y, is_black))

    def update_animation(self):
        self.time += self.delta_time
        for stone in self.stones:
            stone.update(self.delta_time)
        self.update()

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
        
        # Draw stones
        for stone in self.stones:
            self._draw_stone(painter, stone.pos.x(), stone.pos.y(), stone.is_black)

    def _draw_stone(self, painter, x, y, is_black):
        # Draw shadow
        painter.setBrush(QBrush(QColor(0, 0, 0, 40)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(int(x-15), int(y-15), 34, 34)
        
        # Create gradient for stone
        gradient = QRadialGradient(x-5, y-5, 20)
        if is_black:
            gradient.setColorAt(0, QColor(80, 80, 80))
            gradient.setColorAt(0.5, QColor(20, 20, 20))
            gradient.setColorAt(1, QColor(0, 0, 0))
        else:
            gradient.setColorAt(0, QColor(255, 255, 255))
            gradient.setColorAt(0.5, QColor(240, 240, 240))
            gradient.setColorAt(1, QColor(210, 210, 210))
        
        painter.setBrush(gradient)
        painter.drawEllipse(int(x-17), int(y-17), 34, 34)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.stones:
            for stone in self.stones:
                stone.pos = QPointF(
                    random.randint(30, self.width() - 30),
                    random.randint(30, self.height() - 30)
                )
