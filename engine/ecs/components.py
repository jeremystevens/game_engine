
"""
Common ECS components
"""
from ..math.vector2 import Vector2
from ..math.transform import Transform as EngineTransform
from .component import Component


class TransformComponent(Component):
    """Transform component for position, rotation, and scale"""
    
    def __init__(self, position: Vector2 = None, rotation: float = 0.0, scale: Vector2 = None):
        super().__init__()
        self.position = position or Vector2(0, 0)
        self.rotation = rotation
        self.scale = scale or Vector2(1, 1)
        # Create engine transform for compatibility
        self.transform = EngineTransform()
        self.transform.position = self.position
        self.transform.rotation = self.rotation
        self.transform.scale = self.scale
    
    def translate(self, delta: Vector2):
        """Move by delta"""
        self.position += delta
        self.transform.position = self.position
    
    def rotate(self, delta_rotation: float):
        """Rotate by delta"""
        self.rotation += delta_rotation
        self.transform.rotation = self.rotation


class VelocityComponent(Component):
    """Velocity component for movement"""
    
    def __init__(self, velocity: Vector2 = None, max_speed: float = None):
        super().__init__()
        self.velocity = velocity or Vector2(0, 0)
        self.max_speed = max_speed
    
    def limit_speed(self):
        """Limit velocity to max_speed if set"""
        if self.max_speed and self.velocity.magnitude > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed


class SpriteComponent(Component):
    """Sprite component for rendering"""
    
    def __init__(self, color: str = '#FFFFFF', size: Vector2 = None, shape: str = 'rectangle'):
        super().__init__()
        self.color = color
        self.size = size or Vector2(32, 32)
        self.shape = shape
        self.visible = True


class HealthComponent(Component):
    """Health component"""
    
    def __init__(self, max_health: int = 100, current_health: int = None):
        super().__init__()
        self.max_health = max_health
        self.current_health = current_health if current_health is not None else max_health
        self.is_dead = False
    
    def take_damage(self, damage: int):
        """Take damage"""
        self.current_health = max(0, self.current_health - damage)
        if self.current_health <= 0:
            self.is_dead = True
    
    def heal(self, amount: int):
        """Heal by amount"""
        self.current_health = min(self.max_health, self.current_health + amount)
        self.is_dead = False


class TagComponent(Component):
    """Tag component for marking entities"""
    
    def __init__(self, *tags: str):
        super().__init__()
        self.tags = set(tags)
    
    def add_tag(self, tag: str):
        """Add a tag"""
        self.tags.add(tag)
    
    def remove_tag(self, tag: str):
        """Remove a tag"""
        self.tags.discard(tag)
    
    def has_tag(self, tag: str) -> bool:
        """Check if has tag"""
        return tag in self.tags


class TimerComponent(Component):
    """Timer component for time-based events"""
    
    def __init__(self, duration: float, callback=None, repeat: bool = False):
        super().__init__()
        self.duration = duration
        self.current_time = 0.0
        self.callback = callback
        self.repeat = repeat
        self.is_finished = False
    
    def update(self, delta_time: float):
        """Update timer"""
        if not self.is_finished:
            self.current_time += delta_time
            if self.current_time >= self.duration:
                if self.callback:
                    self.callback()
                if self.repeat:
                    self.current_time = 0.0
                else:
                    self.is_finished = True
    
    def reset(self):
        """Reset timer"""
        self.current_time = 0.0
        self.is_finished = False
