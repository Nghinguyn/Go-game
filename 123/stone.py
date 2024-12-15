# src/game/stone.py

from PyQt6.QtCore import QPointF
import math
import random

class Stone:
    def __init__(self, x: float, y: float, is_black: bool):
        self.SPEED_MULTIPLIER = 0.3
        self.GRID_SIZE = 40
        self.MAX_STEPS = 1
        
        self.original_grid_x = round(x / self.GRID_SIZE)
        self.original_grid_y = round(y / self.GRID_SIZE)
        self.is_black = is_black
        
        self.pos = QPointF(x, y)
        self.velocity = QPointF(0, 0)
        
        # Movement parameters
        self.direction = random.uniform(0, 2 * math.pi)
        self.speed = 0.5
        
        # Boundary box
        self.min_x = x - self.GRID_SIZE * self.MAX_STEPS
        self.max_x = x + self.GRID_SIZE * self.MAX_STEPS
        self.min_y = y - self.GRID_SIZE * self.MAX_STEPS
        self.max_y = y + self.GRID_SIZE * self.MAX_STEPS
        
        # Direction change parameters
        self.direction_timer = 0
        self.direction_change_interval = random.uniform(2.0, 4.0)

    def update(self, time: float) -> None:
        # Update direction periodically
        self.direction_timer += time
        if self.direction_timer >= self.direction_change_interval:
            self.direction_timer = 0
            self.direction_change_interval = random.uniform(2.0, 4.0)
            self.direction += random.uniform(-0.5, 0.5)
            
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
