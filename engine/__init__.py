"""
Pure Python 2D Game Engine

A complete game engine built using only Python's standard library.
No external dependencies required!
"""

# Core engine
from .core.engine import GameEngine
from .core.window import Window
from .core.logger import Logger, LogLevel, get_logger

# Math utilities
from .math.vector2 import Vector2
from .math.vector3 import Vector3
from .math.quaternion import Quaternion
from .math.transform import Transform

# Scene management
from .scene.scene import Scene
from .scene.game_object import GameObject

# Graphics
from .graphics.sprite import Sprite
from .graphics.renderer import Renderer

# Input
from .input.input_manager import InputManager

# Audio
from .audio.sound_generator import SoundGenerator

# ECS (Entity Component System)
from .ecs.entity import Entity, EntityManager
from .ecs.component import Component
from .ecs.system import System, SystemManager
from .ecs.world import World
from .ecs.components import (
    TransformComponent, VelocityComponent, SpriteComponent, 
    HealthComponent, TagComponent, TimerComponent
)
from .ecs.systems import (
    MovementSystem, RenderSystem, HealthSystem, 
    TimerSystem, BoundarySystem
)

__version__ = "1.0.0"

__all__ = [
    # Core
    'GameEngine',
    'Window', 
    'Logger',
    'LogLevel',
    'get_logger',

    # Math
    'Vector2',
    'Vector3', 
    'Quaternion',
    'Transform',

    # Scene
    'Scene',
    'GameObject',

    # Graphics
    'Sprite',
    'Renderer',

    # Input
    'InputManager',

    # Audio
    'SoundGenerator',

    # ECS
    'Entity',
    'EntityManager',
    'Component',
    'System',
    'SystemManager',
    'World',
    'TransformComponent',
    'VelocityComponent',
    'SpriteComponent',
    'HealthComponent',
    'TagComponent',
    'TimerComponent',
    'MovementSystem',
    'RenderSystem',
    'HealthSystem',
    'TimerSystem',
    'BoundarySystem'
]