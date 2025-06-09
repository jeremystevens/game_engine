"""
Sprite component for rendering 2D shapes and images
"""
from typing import Optional, Tuple
from ..scene.game_object import Component
from ..math.vector2 import Vector2
from .renderer import Renderer


class Sprite(Component):
    """Sprite component for rendering 2D shapes"""
    
    def __init__(self, color: str = '#FFFFFF', size: Vector2 = None, shape: str = 'rectangle'):
        super().__init__()
        self.color = color
        self.size = size or Vector2(50, 50)
        self.shape = shape  # 'rectangle', 'circle', 'triangle'
        self.outline_color: Optional[str] = None
        self.outline_width = 1
        self.visible = True
        self.alpha = 1.0  # 0.0 to 1.0
        
    def set_color(self, color: str):
        """Set the sprite color"""
        self.color = color
    
    def set_size(self, size: Vector2):
        """Set the sprite size"""
        self.size = size
    
    def set_outline(self, color: str, width: int = 1):
        """Set outline properties"""
        self.outline_color = color
        self.outline_width = width
    
    def set_alpha(self, alpha: float):
        """Set sprite transparency (0.0 to 1.0)"""
        self.alpha = max(0.0, min(1.0, alpha))
    
    def get_size(self) -> Vector2:
        """Get the size of the sprite"""
        return self.size.copy()
    
    def contains_point(self, point: Vector2) -> bool:
        """Check if a point is inside the sprite"""
        if not self.game_object:
            return False
        
        # Get world transform
        world_pos = self.game_object.transform.world_position
        world_scale = self.game_object.transform.world_scale
        
        # Calculate actual size
        actual_size = Vector2(
            self.size.x * world_scale.x,
            self.size.y * world_scale.y
        )
        
        if self.shape == 'circle':
            # Circle collision
            radius = max(actual_size.x, actual_size.y) / 2
            distance = point.distance_to(world_pos)
            return distance <= radius
        else:
            # Rectangle collision (simplified - no rotation)
            half_w = actual_size.x / 2
            half_h = actual_size.y / 2
            
            return (world_pos.x - half_w <= point.x <= world_pos.x + half_w and
                    world_pos.y - half_h <= point.y <= world_pos.y + half_h)
    
    def render(self, renderer: Renderer):
        """Render the sprite"""
        if not self.visible or not self.game_object:
            return
        
        # Get world transform
        transform = self.game_object.transform
        world_pos = transform.world_position
        world_rotation = transform.world_rotation
        world_scale = transform.world_scale
        
        # Calculate actual size
        actual_size = Vector2(
            self.size.x * world_scale.x,
            self.size.y * world_scale.y
        )
        
        # Apply alpha to color (simplified)
        color = self.color
        if self.alpha < 1.0:
            # For simplicity, we'll just use the color as-is
            # In a more advanced renderer, we'd handle alpha blending
            pass
        
        # Render based on shape
        if self.shape == 'circle':
            radius = max(actual_size.x, actual_size.y) / 2
            renderer.draw_circle(
                world_pos, radius, color,
                self.outline_color, self.outline_width
            )
        elif self.shape == 'triangle':
            # Draw triangle as polygon
            half_w = actual_size.x / 2
            half_h = actual_size.y / 2
            
            # Triangle points (local coordinates)
            points = [
                Vector2(0, -half_h),      # Top
                Vector2(-half_w, half_h), # Bottom left
                Vector2(half_w, half_h)   # Bottom right
            ]
            
            # Rotate and translate points
            world_points = []
            for point in points:
                rotated = point.rotate(world_rotation)
                world_point = world_pos + rotated
                world_points.append(world_point)
            
            renderer.draw_polygon(
                world_points, color,
                self.outline_color, self.outline_width
            )
        else:
            # Default to rectangle
            renderer.draw_rectangle(
                world_pos, actual_size, color,
                world_rotation, self.outline_color, self.outline_width
            )