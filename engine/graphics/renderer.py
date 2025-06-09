"""
2D Renderer using tkinter Canvas
"""
import math
from tkinter import Canvas
from typing import Tuple, Optional
from ..math.vector2 import Vector2


class Renderer:
    """2D renderer using tkinter Canvas"""
    
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.width = int(canvas['width'])
        self.height = int(canvas['height'])
        
    def draw_rectangle(self, position: Vector2, size: Vector2, color: str = '#FFFFFF', 
                      rotation: float = 0.0, outline: str = None, width: int = 1):
        """Draw a rectangle"""
        if rotation == 0:
            # Simple case - no rotation
            x1 = position.x - size.x / 2
            y1 = position.y - size.y / 2
            x2 = position.x + size.x / 2
            y2 = position.y + size.y / 2
            
            return self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline=outline or color,
                width=width
            )
        else:
            # Rotated rectangle - draw as polygon
            half_w = size.x / 2
            half_h = size.y / 2
            
            # Rectangle corners (local coordinates)
            corners = [
                Vector2(-half_w, -half_h),
                Vector2(half_w, -half_h),
                Vector2(half_w, half_h),
                Vector2(-half_w, half_h)
            ]
            
            # Rotate and translate corners
            rotated_corners = []
            for corner in corners:
                rotated = corner.rotate(rotation)
                world_pos = position + rotated
                rotated_corners.extend([world_pos.x, world_pos.y])
            
            return self.canvas.create_polygon(
                rotated_corners,
                fill=color,
                outline=outline or color,
                width=width
            )
    
    def draw_circle(self, position: Vector2, radius: float, color: str = '#FFFFFF',
                   outline: str = None, width: int = 1):
        """Draw a circle"""
        x1 = position.x - radius
        y1 = position.y - radius
        x2 = position.x + radius
        y2 = position.y + radius
        
        return self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=color,
            outline=outline or color,
            width=width
        )
    
    def draw_line(self, start: Vector2, end: Vector2, color: str = '#FFFFFF', width: int = 1):
        """Draw a line"""
        return self.canvas.create_line(
            start.x, start.y, end.x, end.y,
            fill=color,
            width=width
        )
    
    def draw_text(self, position: Vector2, text: str, color: str = '#FFFFFF',
                 font: Tuple[str, int] = ('Arial', 12)):
        """Draw text"""
        return self.canvas.create_text(
            position.x, position.y,
            text=text,
            fill=color,
            font=font
        )
    
    def draw_polygon(self, points: list, color: str = '#FFFFFF',
                    outline: str = None, width: int = 1):
        """Draw a polygon from a list of Vector2 points"""
        coords = []
        for point in points:
            coords.extend([point.x, point.y])
        
        return self.canvas.create_polygon(
            coords,
            fill=color,
            outline=outline or color,
            width=width
        )
    
    def clear(self):
        """Clear all drawn objects"""
        self.canvas.delete("all")
    
    def get_size(self) -> Vector2:
        """Get renderer size"""
        return Vector2(self.width, self.height)
    
    def get_center(self) -> Vector2:
        """Get center point"""
        return Vector2(self.width / 2, self.height / 2)