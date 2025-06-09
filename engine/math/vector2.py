"""
2D Vector implementation with comprehensive math operations
"""
import math
from typing import Union, Tuple


class Vector2:
    """2D Vector class with mathematical operations"""
    
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)
    
    def __str__(self) -> str:
        return f"Vector2({self.x:.2f}, {self.y:.2f})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: Union[float, int]) -> 'Vector2':
        return Vector2(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: Union[float, int]) -> 'Vector2':
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: Union[float, int]) -> 'Vector2':
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector2(self.x / scalar, self.y / scalar)
    
    def __eq__(self, other: 'Vector2') -> bool:
        return abs(self.x - other.x) < 1e-6 and abs(self.y - other.y) < 1e-6
    
    def copy(self) -> 'Vector2':
        """Create a copy of this vector"""
        return Vector2(self.x, self.y)
    
    @property
    def magnitude(self) -> float:
        """Get the magnitude (length) of the vector"""
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    @property
    def magnitude_squared(self) -> float:
        """Get the squared magnitude (faster than magnitude)"""
        return self.x * self.x + self.y * self.y
    
    def normalize(self) -> 'Vector2':
        """Return a normalized version of this vector"""
        mag = self.magnitude
        if mag == 0:
            return Vector2(0, 0)
        return Vector2(self.x / mag, self.y / mag)
    
    def normalized(self) -> 'Vector2':
        """Alias for normalize()"""
        return self.normalize()
    
    def dot(self, other: 'Vector2') -> float:
        """Calculate dot product with another vector"""
        return self.x * other.x + self.y * other.y
    
    def cross(self, other: 'Vector2') -> float:
        """Calculate 2D cross product (returns scalar)"""
        return self.x * other.y - self.y * other.x
    
    def distance_to(self, other: 'Vector2') -> float:
        """Calculate distance to another vector"""
        return (self - other).magnitude
    
    def distance_squared_to(self, other: 'Vector2') -> float:
        """Calculate squared distance to another vector (faster)"""
        return (self - other).magnitude_squared
    
    def angle_to(self, other: 'Vector2') -> float:
        """Calculate angle to another vector in radians"""
        dot_product = self.dot(other)
        mag_product = self.magnitude * other.magnitude
        if mag_product == 0:
            return 0
        return math.acos(max(-1, min(1, dot_product / mag_product)))
    
    def rotate(self, angle: float) -> 'Vector2':
        """Rotate vector by angle in radians"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return Vector2(
            self.x * cos_a - self.y * sin_a,
            self.x * sin_a + self.y * cos_a
        )
    
    def lerp(self, other: 'Vector2', t: float) -> 'Vector2':
        """Linear interpolation between this and another vector"""
        t = max(0, min(1, t))  # Clamp t between 0 and 1
        return self + (other - self) * t
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple (x, y)"""
        return (self.x, self.y)
    
    def to_int_tuple(self) -> Tuple[int, int]:
        """Convert to integer tuple"""
        return (int(self.x), int(self.y))
    
    @staticmethod
    def zero() -> 'Vector2':
        """Return zero vector"""
        return Vector2(0, 0)
    
    @staticmethod
    def one() -> 'Vector2':
        """Return unit vector (1, 1)"""
        return Vector2(1, 1)
    
    @staticmethod
    def up() -> 'Vector2':
        """Return up vector (0, -1) - negative Y is up in screen coordinates"""
        return Vector2(0, -1)
    
    @staticmethod
    def down() -> 'Vector2':
        """Return down vector (0, 1)"""
        return Vector2(0, 1)
    
    @staticmethod
    def left() -> 'Vector2':
        """Return left vector (-1, 0)"""
        return Vector2(-1, 0)
    
    @staticmethod
    def right() -> 'Vector2':
        """Return right vector (1, 0)"""
        return Vector2(1, 0)
    
    @staticmethod
    def from_angle(angle: float, magnitude: float = 1.0) -> 'Vector2':
        """Create vector from angle and magnitude"""
        return Vector2(
            math.cos(angle) * magnitude,
            math.sin(angle) * magnitude
        )
    
    def to_vector3(self, z: float = 0.0) -> 'Vector3':
        """Convert to Vector3 with optional z component"""
        from .vector3 import Vector3
        return Vector3(self.x, self.y, z)