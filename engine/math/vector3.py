
"""
3D Vector implementation for extended math operations
"""
import math
from typing import Union, Tuple
from .vector2 import Vector2


class Vector3:
    """3D Vector class with mathematical operations"""
    
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __str__(self) -> str:
        return f"Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: Union[float, int]) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar: Union[float, int]) -> 'Vector3':
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: Union[float, int]) -> 'Vector3':
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def __eq__(self, other: 'Vector3') -> bool:
        return (abs(self.x - other.x) < 1e-6 and 
                abs(self.y - other.y) < 1e-6 and 
                abs(self.z - other.z) < 1e-6)
    
    def copy(self) -> 'Vector3':
        """Create a copy of this vector"""
        return Vector3(self.x, self.y, self.z)
    
    @property
    def magnitude(self) -> float:
        """Get the magnitude (length) of the vector"""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    @property
    def magnitude_squared(self) -> float:
        """Get the squared magnitude (faster than magnitude)"""
        return self.x * self.x + self.y * self.y + self.z * self.z
    
    def normalize(self) -> 'Vector3':
        """Return a normalized version of this vector"""
        mag = self.magnitude
        if mag == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)
    
    def normalized(self) -> 'Vector3':
        """Alias for normalize()"""
        return self.normalize()
    
    def dot(self, other: 'Vector3') -> float:
        """Calculate dot product with another vector"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3') -> 'Vector3':
        """Calculate 3D cross product with another vector"""
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def distance_to(self, other: 'Vector3') -> float:
        """Calculate distance to another vector"""
        return (self - other).magnitude
    
    def distance_squared_to(self, other: 'Vector3') -> float:
        """Calculate squared distance to another vector (faster)"""
        return (self - other).magnitude_squared
    
    def angle_to(self, other: 'Vector3') -> float:
        """Calculate angle to another vector in radians"""
        dot_product = self.dot(other)
        mag_product = self.magnitude * other.magnitude
        if mag_product == 0:
            return 0
        return math.acos(max(-1, min(1, dot_product / mag_product)))
    
    def lerp(self, other: 'Vector3', t: float) -> 'Vector3':
        """Linear interpolation between this and another vector"""
        t = max(0, min(1, t))  # Clamp t between 0 and 1
        return self + (other - self) * t
    
    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert to tuple (x, y, z)"""
        return (self.x, self.y, self.z)
    
    def to_vector2(self) -> Vector2:
        """Convert to Vector2 (drops z component)"""
        return Vector2(self.x, self.y)
    
    def project_onto_plane(self, plane_normal: 'Vector3') -> 'Vector3':
        """Project this vector onto a plane defined by its normal"""
        normal = plane_normal.normalized()
        return self - normal * self.dot(normal)
    
    def reflect(self, normal: 'Vector3') -> 'Vector3':
        """Reflect this vector across a surface with given normal"""
        normal = normal.normalized()
        return self - 2 * self.dot(normal) * normal
    
    @staticmethod
    def zero() -> 'Vector3':
        """Return zero vector"""
        return Vector3(0, 0, 0)
    
    @staticmethod
    def one() -> 'Vector3':
        """Return unit vector (1, 1, 1)"""
        return Vector3(1, 1, 1)
    
    @staticmethod
    def up() -> 'Vector3':
        """Return up vector (0, 1, 0)"""
        return Vector3(0, 1, 0)
    
    @staticmethod
    def down() -> 'Vector3':
        """Return down vector (0, -1, 0)"""
        return Vector3(0, -1, 0)
    
    @staticmethod
    def left() -> 'Vector3':
        """Return left vector (-1, 0, 0)"""
        return Vector3(-1, 0, 0)
    
    @staticmethod
    def right() -> 'Vector3':
        """Return right vector (1, 0, 0)"""
        return Vector3(1, 0, 0)
    
    @staticmethod
    def forward() -> 'Vector3':
        """Return forward vector (0, 0, 1)"""
        return Vector3(0, 0, 1)
    
    @staticmethod
    def back() -> 'Vector3':
        """Return back vector (0, 0, -1)"""
        return Vector3(0, 0, -1)
    
    @staticmethod
    def from_vector2(vec2: Vector2, z: float = 0.0) -> 'Vector3':
        """Create Vector3 from Vector2 with optional z component"""
        return Vector3(vec2.x, vec2.y, z)
