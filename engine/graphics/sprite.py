"""
Sprite component for rendering 2D shapes and images
"""
import time
from typing import Optional, Tuple, List, Dict
from ..scene.game_object import Component
from ..math.vector2 import Vector2
from .renderer import Renderer


class SpriteAnimation:
    """Animation data for sprites"""
    
    def __init__(self, name: str, frame_indices: List[int], frame_duration: float = 0.1, loop: bool = True):
        self.name = name
        self.frame_indices = frame_indices
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.frame_timer = 0.0
        self.is_playing = False
    
    def update(self, delta_time: float) -> int:
        """Update animation and return current frame index"""
        if not self.is_playing or not self.frame_indices:
            return self.frame_indices[0] if self.frame_indices else 0
        
        self.frame_timer += delta_time
        
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0.0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frame_indices):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frame_indices) - 1
                    self.is_playing = False
        
        return self.frame_indices[self.current_frame]
    
    def play(self):
        """Start playing the animation"""
        self.is_playing = True
    
    def stop(self):
        """Stop the animation"""
        self.is_playing = False
        self.current_frame = 0
        self.frame_timer = 0.0
    
    def pause(self):
        """Pause the animation"""
        self.is_playing = False


class SpriteAtlas:
    """Sprite atlas for efficient texture management"""
    
    def __init__(self, texture_size: Vector2):
        self.texture_size = texture_size
        self.sprites: Dict[str, Dict] = {}
    
    def add_sprite(self, name: str, position: Vector2, size: Vector2, color: str = '#FFFFFF'):
        """Add a sprite region to the atlas"""
        self.sprites[name] = {
            'position': position,
            'size': size,
            'color': color,
            'uv_start': Vector2(position.x / self.texture_size.x, position.y / self.texture_size.y),
            'uv_end': Vector2((position.x + size.x) / self.texture_size.x, (position.y + size.y) / self.texture_size.y)
        }
    
    def get_sprite_data(self, name: str) -> Optional[Dict]:
        """Get sprite data by name"""
        return self.sprites.get(name)
    
    def create_animation_frames(self, base_name: str, frame_count: int, frame_size: Vector2, 
                              start_position: Vector2, horizontal: bool = True) -> List[str]:
        """Create animation frames from a sprite sheet"""
        frame_names = []
        
        for i in range(frame_count):
            frame_name = f"{base_name}_frame_{i}"
            
            if horizontal:
                frame_pos = Vector2(start_position.x + i * frame_size.x, start_position.y)
            else:
                frame_pos = Vector2(start_position.x, start_position.y + i * frame_size.y)
            
            self.add_sprite(frame_name, frame_pos, frame_size)
            frame_names.append(frame_name)
        
        return frame_names


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
        
        # Animation system
        self.animations: Dict[str, SpriteAnimation] = {}
        self.current_animation: Optional[SpriteAnimation] = None
        self.sprite_atlas: Optional[SpriteAtlas] = None
        self.current_sprite_name: Optional[str] = None
        
        # Shader effects
        self.shader_effects: Dict[str, any] = {}
        self.tint_color: Optional[str] = None
        self.brightness = 1.0
        self.contrast = 1.0
        
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
    
    def add_animation(self, name: str, frame_indices: List[int], frame_duration: float = 0.1, loop: bool = True):
        """Add an animation to this sprite"""
        self.animations[name] = SpriteAnimation(name, frame_indices, frame_duration, loop)
    
    def play_animation(self, name: str):
        """Play a specific animation"""
        if name in self.animations:
            if self.current_animation:
                self.current_animation.stop()
            self.current_animation = self.animations[name]
            self.current_animation.play()
    
    def stop_animation(self):
        """Stop current animation"""
        if self.current_animation:
            self.current_animation.stop()
            self.current_animation = None
    
    def set_sprite_atlas(self, atlas: SpriteAtlas, sprite_name: str = None):
        """Set sprite atlas and optionally select a sprite"""
        self.sprite_atlas = atlas
        if sprite_name:
            self.current_sprite_name = sprite_name
    
    def set_current_sprite(self, sprite_name: str):
        """Set current sprite from atlas"""
        if self.sprite_atlas and sprite_name in self.sprite_atlas.sprites:
            self.current_sprite_name = sprite_name
    
    def set_tint(self, color: str):
        """Set tint color for shader effect"""
        self.tint_color = color
    
    def set_brightness(self, brightness: float):
        """Set brightness (0.0 to 2.0, 1.0 is normal)"""
        self.brightness = max(0.0, min(2.0, brightness))
    
    def set_contrast(self, contrast: float):
        """Set contrast (0.0 to 2.0, 1.0 is normal)"""
        self.contrast = max(0.0, min(2.0, contrast))
    
    def add_shader_effect(self, name: str, effect_data: any):
        """Add a custom shader effect"""
        self.shader_effects[name] = effect_data
    
    def remove_shader_effect(self, name: str):
        """Remove a shader effect"""
        if name in self.shader_effects:
            del self.shader_effects[name]
    
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
    
    def update(self, delta_time: float):
        """Update sprite animations"""
        if self.current_animation:
            frame_index = self.current_animation.update(delta_time)
            # If using atlas, update current sprite based on animation frame
            if self.sprite_atlas and self.current_animation.frame_indices:
                frame_name = f"{self.current_animation.name}_frame_{frame_index}"
                if frame_name in self.sprite_atlas.sprites:
                    self.current_sprite_name = frame_name
    
    def render(self, renderer: Renderer):
        """Render the sprite"""
        if not self.visible or not self.game_object:
            return
        
        # Get world transform
        transform = self.game_object.transform
        world_pos = transform.world_position
        world_rotation = transform.world_rotation
        world_scale = transform.world_scale
        
        # Determine color and size based on atlas or default
        render_color = self.color
        render_size = self.size
        
        if self.sprite_atlas and self.current_sprite_name:
            sprite_data = self.sprite_atlas.get_sprite_data(self.current_sprite_name)
            if sprite_data:
                render_color = sprite_data['color']
                render_size = sprite_data['size']
        
        # Calculate actual size
        actual_size = Vector2(
            render_size.x * world_scale.x,
            render_size.y * world_scale.y
        )
        
        # Apply shader effects
        final_color = self._apply_shader_effects(render_color)
        
        # Render based on shape
        if self.shape == 'circle':
            radius = max(actual_size.x, actual_size.y) / 2
            renderer.draw_circle(
                world_pos, radius, final_color,
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
                world_points, final_color,
                self.outline_color, self.outline_width
            )
        else:
            # Default to rectangle
            renderer.draw_rectangle(
                world_pos, actual_size, final_color,
                world_rotation, self.outline_color, self.outline_width
            )
    
    def _apply_shader_effects(self, base_color: str) -> str:
        """Apply shader effects to the base color"""
        # Simple shader effect simulation
        color = base_color
        
        # Apply tint
        if self.tint_color:
            color = self._blend_colors(color, self.tint_color, 0.5)
        
        # Brightness and contrast would typically be applied in a real shader
        # For simplicity, we'll just return the color
        return color
    
    def _blend_colors(self, color1: str, color2: str, factor: float) -> str:
        """Simple color blending (simplified implementation)"""
        # In a real implementation, this would properly blend RGB values
        # For now, just return the tint color if factor > 0.5, else base color
        return color2 if factor > 0.5 else color1