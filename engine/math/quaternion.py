
"""
Quaternion implementation for 3D rotations
"""
import math
from typing import Tuple
from .vector3 import Vector3


class Quaternion:
    """Quaternion class for representing 3D rotations"""
    
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)
    
    def __str__(self) -> str:
        return f"Quaternion({self.x:.3f}, {self.y:.3f}, {self.z:.3f}, {self.w:.3f})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __add__(self, other: 'Quaternion') -> 'Quaternion':
        return Quaternion(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
    
    def __sub__(self, other: 'Quaternion') -> 'Quaternion':
        return Quaternion(self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w)
    
    def __mul__(self, other) -> 'Quaternion':
        if isinstance(other, Quaternion):
            # Quaternion multiplication
            return Quaternion(
                self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
                self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
                self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
                self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            )
        else:
            # Scalar multiplication
            return Quaternion(self.x * other, self.y * other, self.z * other, self.w * other)
    
    def __rmul__(self, scalar: float) -> 'Quaternion':
        return self.__mul__(scalar)
    
    def __eq__(self, other: 'Quaternion') -> bool:
        return (abs(self.x - other.x) < 1e-6 and 
                abs(self.y - other.y) < 1e-6 and 
                abs(self.z - other.z) < 1e-6 and 
                abs(self.w - other.w) < 1e-6)
    
    def copy(self) -> 'Quaternion':
        """Create a copy of this quaternion"""
        return Quaternion(self.x, self.y, self.z, self.w)
    
    @property
    def magnitude(self) -> float:
        """Get the magnitude of the quaternion"""
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
    
    @property
    def magnitude_squared(self) -> float:
        """Get the squared magnitude (faster than magnitude)"""
        return self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w
    
    def normalize(self) -> 'Quaternion':
        """Return a normalized version of this quaternion"""
        mag = self.magnitude
        if mag == 0:
            return Quaternion.identity()
        return Quaternion(self.x / mag, self.y / mag, self.z / mag, self.w / mag)
    
    def normalized(self) -> 'Quaternion':
        """Alias for normalize()"""
        return self.normalize()
    
    def conjugate(self) -> 'Quaternion':
        """Return the conjugate of this quaternion"""
        return Quaternion(-self.x, -self.y, -self.z, self.w)
    
    def inverse(self) -> 'Quaternion':
        """Return the inverse of this quaternion"""
        mag_sq = self.magnitude_squared
        if mag_sq == 0:
            return Quaternion.identity()
        conj = self.conjugate()
        return Quaternion(conj.x / mag_sq, conj.y / mag_sq, conj.z / mag_sq, conj.w / mag_sq)
    
    def dot(self, other: 'Quaternion') -> float:
        """Calculate dot product with another quaternion"""
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w
    
    def rotate_vector(self, vector: Vector3) -> Vector3:
        """Rotate a vector by this quaternion"""
        # Convert vector to quaternion
        vec_quat = Quaternion(vector.x, vector.y, vector.z, 0)
        
        # Apply rotation: q * v * q^-1
        result = self * vec_quat * self.inverse()
        
        return Vector3(result.x, result.y, result.z)
    
    def to_euler_angles(self) -> Tuple[float, float, float]:
        """Convert quaternion to Euler angles (roll, pitch, yaw) in radians"""
        # Roll (x-axis rotation)
        sinr_cosp = 2 * (self.w * self.x + self.y * self.z)
        cosr_cosp = 1 - 2 * (self.x * self.x + self.y * self.y)
        roll = math.atan2(sinr_cosp, cosr_cosp)
        
        # Pitch (y-axis rotation)
        sinp = 2 * (self.w * self.y - self.z * self.x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)  # Use 90 degrees if out of range
        else:
            pitch = math.asin(sinp)
        
        # Yaw (z-axis rotation)
        siny_cosp = 2 * (self.w * self.z + self.x * self.y)
        cosy_cosp = 1 - 2 * (self.y * self.y + self.z * self.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        return (roll, pitch, yaw)
    
    def to_axis_angle(self) -> Tuple[Vector3, float]:
        """Convert quaternion to axis-angle representation"""
        if self.w > 1:
            self = self.normalized()
        
        angle = 2 * math.acos(self.w)
        s = math.sqrt(1 - self.w * self.w)
        
        if s < 1e-6:
            # If s is close to zero, direction of axis not important
            axis = Vector3(self.x, self.y, self.z)
        else:
            axis = Vector3(self.x / s, self.y / s, self.z / s)
        
        return (axis, angle)
    
    def lerp(self, other: 'Quaternion', t: float) -> 'Quaternion':
        """Linear interpolation between quaternions (not recommended for rotation)"""
        t = max(0, min(1, t))
        return (self * (1 - t) + other * t).normalized()
    
    def slerp(self, other: 'Quaternion', t: float) -> 'Quaternion':
        """Spherical linear interpolation between quaternions"""
        t = max(0, min(1, t))
        
        dot = self.dot(other)
        
        # If the dot product is negative, the quaternions represent the same rotation
        # but are on opposite sides of the 4D sphere, so we negate one
        if dot < 0:
            other = other * -1
            dot = -dot
        
        # If the quaternions are very similar, use linear interpolation
        if dot > 0.9995:
            return self.lerp(other, t)
        
        # Calculate angle between quaternions
        theta_0 = math.acos(abs(dot))
        sin_theta_0 = math.sin(theta_0)
        
        theta = theta_0 * t
        sin_theta = math.sin(theta)
        
        s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
        s1 = sin_theta / sin_theta_0
        
        return (self * s0 + other * s1).normalized()
    
    @staticmethod
    def identity() -> 'Quaternion':
        """Return identity quaternion (no rotation)"""
        return Quaternion(0, 0, 0, 1)
    
    @staticmethod
    def from_euler_angles(roll: float, pitch: float, yaw: float) -> 'Quaternion':
        """Create quaternion from Euler angles (in radians)"""
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        
        return Quaternion(
            sr * cp * cy - cr * sp * sy,
            cr * sp * cy + sr * cp * sy,
            cr * cp * sy - sr * sp * cy,
            cr * cp * cy + sr * sp * sy
        )
    
    @staticmethod
    def from_axis_angle(axis: Vector3, angle: float) -> 'Quaternion':
        """Create quaternion from axis-angle representation"""
        axis = axis.normalized()
        half_angle = angle * 0.5
        sin_half = math.sin(half_angle)
        
        return Quaternion(
            axis.x * sin_half,
            axis.y * sin_half,
            axis.z * sin_half,
            math.cos(half_angle)
        )
    
    @staticmethod
    def from_rotation_matrix(matrix) -> 'Quaternion':
        """Create quaternion from 3x3 rotation matrix (expects 9-element list/tuple)"""
        # Assumes matrix is [m00, m01, m02, m10, m11, m12, m20, m21, m22]
        trace = matrix[0] + matrix[4] + matrix[8]
        
        if trace > 0:
            s = math.sqrt(trace + 1.0) * 2  # s = 4 * qw
            w = 0.25 * s
            x = (matrix[7] - matrix[5]) / s
            y = (matrix[2] - matrix[6]) / s
            z = (matrix[3] - matrix[1]) / s
        elif matrix[0] > matrix[4] and matrix[0] > matrix[8]:
            s = math.sqrt(1.0 + matrix[0] - matrix[4] - matrix[8]) * 2  # s = 4 * qx
            w = (matrix[7] - matrix[5]) / s
            x = 0.25 * s
            y = (matrix[1] + matrix[3]) / s
            z = (matrix[2] + matrix[6]) / s
        elif matrix[4] > matrix[8]:
            s = math.sqrt(1.0 + matrix[4] - matrix[0] - matrix[8]) * 2  # s = 4 * qy
            w = (matrix[2] - matrix[6]) / s
            x = (matrix[1] + matrix[3]) / s
            y = 0.25 * s
            z = (matrix[5] + matrix[7]) / s
        else:
            s = math.sqrt(1.0 + matrix[8] - matrix[0] - matrix[4]) * 2  # s = 4 * qz
            w = (matrix[3] - matrix[1]) / s
            x = (matrix[2] + matrix[6]) / s
            y = (matrix[5] + matrix[7]) / s
            z = 0.25 * s
        
        return Quaternion(x, y, z, w)
    
    @staticmethod
    def look_rotation(forward: Vector3, up: Vector3 = None) -> 'Quaternion':
        """Create quaternion that rotates forward to look in the given direction"""
        if up is None:
            up = Vector3.up()
        
        forward = forward.normalized()
        up = up.normalized()
        
        right = up.cross(forward).normalized()
        up = forward.cross(right)
        
        # Create rotation matrix and convert to quaternion
        matrix = [
            right.x, up.x, forward.x,
            right.y, up.y, forward.y,
            right.z, up.z, forward.z
        ]
        
        return Quaternion.from_rotation_matrix(matrix)
