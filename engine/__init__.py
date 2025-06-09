"""
Pure Python 2D Game Engine - Built completely from scratch
No external dependencies - uses only Python standard library
"""

from .core.engine import GameEngine
from .core.window import Window
from .scene.game_object import GameObject
from .scene.scene import Scene
from .math.vector2 import Vector2
from .math.transform import Transform
from .graphics.renderer import Renderer
from .graphics.sprite import Sprite
from .input.input_manager import InputManager

__version__ = "1.0.0"
__all__ = [
    'GameEngine',
    'Window', 
    'GameObject',
    'Scene',
    'Vector2',
    'Transform',
    'Renderer',
    'Sprite',
    'InputManager'
]