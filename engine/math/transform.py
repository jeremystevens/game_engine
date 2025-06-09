"""
Transform component for position, rotation, and scale
"""
from .vector2 import Vector2
import math


class Transform:
    """Transform component handling position, rotation, and scale"""
    
    def __init__(self, position: Vector2 = None, rotation: float = 0.0, scale: Vector2 = None):
        self.position = position or Vector2.zero()
        self.rotation = rotation  # In radians
        self.scale = scale or Vector2.one()
        self._parent = None
        self._children = []
        
        # 3D support (optional)
        self._quaternion_rotation = None
        self._use_3d = False
    
    def __str__(self) -> str:
        return f"Transform(pos={self.position}, rot={math.degrees(self.rotation):.1f}°, scale={self.scale})"
    
    @property
    def parent(self):
        """Get parent transform"""
        return self._parent
    
    @parent.setter
    def parent(self, parent_transform):
        """Set parent transform"""
        if self._parent:
            self._parent._children.remove(self)
        
        self._parent = parent_transform
        if parent_transform:
            parent_transform._children.append(self)
    
    @property
    def children(self):
        """Get list of child transforms"""
        return list(self._children)  # Return copy to prevent external modification
    
    @property
    def world_position(self) -> Vector2:
        """Get world position (considering parent transforms)"""
        if not self._parent:
            return self.position.copy()
        
        # Apply parent's transform
        parent_world = self._parent.world_position
        parent_rotation = self._parent.world_rotation
        parent_scale = self._parent.world_scale
        
        # Scale and rotate local position, then add parent position
        scaled_pos = Vector2(self.position.x * parent_scale.x, self.position.y * parent_scale.y)
        rotated_pos = scaled_pos.rotate(parent_rotation)
        return parent_world + rotated_pos
    
    @property
    def world_rotation(self) -> float:
        """Get world rotation (considering parent transforms)"""
        if not self._parent:
            return self.rotation
        return self._parent.world_rotation + self.rotation
    
    @property
    def world_scale(self) -> Vector2:
        """Get world scale (considering parent transforms)"""
        if not self._parent:
            return self.scale.copy()
        
        parent_scale = self._parent.world_scale
        return Vector2(self.scale.x * parent_scale.x, self.scale.y * parent_scale.y)
    
    def translate(self, delta: Vector2):
        """Move by delta vector"""
        self.position += delta
    
    def rotate(self, delta_rotation: float):
        """Rotate by delta angle in radians"""
        self.rotation += delta_rotation
    
    def scale_by(self, scale_factor: Vector2):
        """Scale by factor"""
        self.scale = Vector2(self.scale.x * scale_factor.x, self.scale.y * scale_factor.y)
    
    def look_at(self, target: Vector2):
        """Rotate to look at target position"""
        direction = target - self.world_position
        self.rotation = math.atan2(direction.y, direction.x)
    
    def forward(self) -> Vector2:
        """Get forward direction vector"""
        return Vector2.from_angle(self.world_rotation)
    
    def right(self) -> Vector2:
        """Get right direction vector"""
        return Vector2.from_angle(self.world_rotation + math.pi / 2)
    
    def transform_point(self, local_point: Vector2) -> Vector2:
        """Transform a local point to world space"""
        world_scale = self.world_scale
        world_rotation = self.world_rotation
        world_position = self.world_position
        
        # Scale, then rotate, then translate
        scaled = Vector2(local_point.x * world_scale.x, local_point.y * world_scale.y)
        rotated = scaled.rotate(world_rotation)
        return world_position + rotated
    
    def inverse_transform_point(self, world_point: Vector2) -> Vector2:
        """Transform a world point to local space"""
        world_scale = self.world_scale
        world_rotation = self.world_rotation
        world_position = self.world_position
        
        # Translate, then rotate back, then scale back
        translated = world_point - world_position
        rotated = translated.rotate(-world_rotation)
        return Vector2(rotated.x / world_scale.x, rotated.y / world_scale.y)
    
    # 3D Transform Support
    def enable_3d(self):
        """Enable 3D transform capabilities"""
        self._use_3d = True
        if self._quaternion_rotation is None:
            from .quaternion import Quaternion
            self._quaternion_rotation = Quaternion.identity()
    
    def disable_3d(self):
        """Disable 3D transform capabilities"""
        self._use_3d = False
        self._quaternion_rotation = None
    
    @property
    def quaternion_rotation(self):
        """Get quaternion rotation (3D mode only)"""
        if not self._use_3d:
            return None
        return self._quaternion_rotation
    
    @quaternion_rotation.setter
    def quaternion_rotation(self, quat):
        """Set quaternion rotation (enables 3D mode)"""
        if not self._use_3d:
            self.enable_3d()
        self._quaternion_rotation = quat
    
    def set_rotation_from_quaternion(self, quaternion):
        """Set 2D rotation from quaternion's Z rotation"""
        if quaternion:
            euler = quaternion.to_euler_angles()
            self.rotation = euler[2]  # Use yaw for 2D rotation
    
    def get_quaternion_from_rotation(self):
        """Get quaternion representation of current 2D rotation"""
        from .quaternion import Quaternion
        from .vector3 import Vector3
        return Quaternion.from_axis_angle(Vector3(0, 0, 1), self.rotation)