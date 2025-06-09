# Pure Python 2D Game Engine - Built Completely from Scratch

A comprehensive 2D game engine built entirely from scratch using **only Python's standard library**. No external dependencies like pygame, OpenGL, or any third-party graphics libraries. This engine demonstrates how to create a complete game development framework using pure Python and tkinter for cross-platform windowing.

## 🎯 Philosophy

This project proves that you can build sophisticated game engines without relying on external libraries. Every component - from vector mathematics to input handling to graphics rendering - is implemented from the ground up using only Python's built-in modules.

## ✨ Features

### Core Engine
- **Pure Python Implementation**: Zero external dependencies beyond Python standard library
- **Cross-Platform**: Uses tkinter for universal compatibility across Windows, macOS, and Linux
- **Game Engine Architecture**: Professional game engine design patterns and structure
- **Fixed Timestep Game Loop**: Consistent physics and animation regardless of framerate
- **2D/3D Hybrid Support**: Optional 3D mathematics with 2D rendering capabilities

### Scene System
- **Scene Management**: Organize game objects into scenes with lifecycle management
- **GameObject Architecture**: Component-based game objects with transform hierarchy
- **Component System**: Modular components for extending game object functionality
- **Object Pooling**: Efficient memory management for game objects

### Mathematics (Built from Scratch)
- **Vector2**: Comprehensive 2D vector implementation with all standard operations
- **Vector3**: Full 3D vector mathematics with cross product, magnitude, and transformations
- **Transform System**: 2D/3D position, rotation, and scale with parent-child relationships
- **Quaternion Support**: 3D rotation support with quaternion mathematics (optional 3D mode)
- **Advanced Math**: Dot product, cross product, interpolation, and coordinate transformations
- **Collision Detection**: Point-in-shape and basic collision detection

### Graphics Rendering
- **Custom 2D Renderer**: Built on tkinter Canvas with advanced drawing capabilities
- **Shape Rendering**: Rectangles, circles, triangles, and custom polygons
- **Transform Support**: Full rotation, scaling, and translation for all shapes
- **Color Management**: RGB color support with outline and fill options
- **Z-Ordering**: Proper layering system for depth sorting

### Input Handling
- **Keyboard Input**: Complete keyboard state management with key press detection
- **Mouse Input**: Mouse position, button states, and click detection
- **Input Utilities**: Convenience methods for common input patterns (WASD, arrows)
- **Event-Driven**: Proper event handling with frame-accurate input detection

### Audio System
- **Procedural Sound Generation**: Create sound effects using mathematical waveforms
- **Multiple Wave Types**: Support for sine, square, sawtooth, triangle, and noise waves
- **Sound Effects**: Built-in generators for bullets, explosions, and engine sounds
- **No External Dependencies**: Audio system built entirely with Python standard library
- **Real-time Playback**: Thread-based sound playback system

### Logging System
- **Multi-Level Logging**: Support for DEBUG, INFO, WARNING, and ERROR levels
- **Console and File Output**: Log to console with optional file logging
- **Performance Monitoring**: Built-in FPS tracking and engine performance metrics
- **Color-Coded Output**: Visual distinction between log levels in console
- **Configurable Verbosity**: Adjustable logging levels for development and production

### ECS (Entity Component System)
- **Pure ECS Architecture**: Complete Entity Component System implementation
- **Entity Management**: Lightweight entities as simple ID containers
- **Component System**: Data-only components for position, velocity, sprites, health, and more
- **System Processing**: Logic systems that process entities with specific component combinations
- **Performance Optimized**: Efficient component queries and batch processing
- **Modular Design**: Easy to extend with custom components and systems

### Hot-Reload System
- **Live Script Reloading**: Automatically reload Python scripts when they change on disk
- **Development Workflow**: Instant feedback during development without restarting the game
- **File Monitoring**: Efficient file system watching using Python's built-in modules
- **Error Handling**: Graceful error handling when reload fails, with detailed error reporting
- **Selective Reloading**: Choose which scripts to monitor and reload

## 🏗️ Project Structure

```
engine/
├── __init__.py              # Main engine exports
├── core/
│   ├── __init__.py
│   ├── engine.py           # Main GameEngine class
│   ├── hot_reload.py       # Live script reloading system
│   ├── logger.py           # Logging system
│   └── window.py           # Cross-platform window management
├── scene/
│   ├── __init__.py
│   ├── scene.py            # Scene management
│   └── game_object.py      # GameObject and Component classes
├── math/
│   ├── __init__.py
│   ├── vector2.py          # 2D vector mathematics
│   ├── vector3.py          # 3D vector mathematics
│   ├── quaternion.py       # 3D rotation quaternions
│   └── transform.py        # 2D/3D transform component
├── graphics/
│   ├── __init__.py
│   ├── renderer.py         # 2D rendering system
│   └── sprite.py           # Sprite rendering component
├── input/
│   ├── __init__.py
│   └── input_manager.py     # Input handling system
├── audio/
│   ├── __init__.py
│   └── sound_generator.py   # Procedural sound generation
└── ecs/
    ├── __init__.py
    ├── entity.py           # Entity and EntityManager
    ├── component.py        # Base component class
    ├── components.py       # Common components (Transform, Velocity, etc.)
    ├── system.py           # System and SystemManager
    ├── systems.py          # Common systems (Movement, Render, etc.)
    └── world.py            # ECS World management
```

## 🚀 Installation

**No installation required!** This engine uses only Python's standard library.

Requirements:
- Python 3.7 or higher
- tkinter (included with most Python installations)

## 🎮 Quick Start

```python
from engine import GameEngine, GameObject, Vector2, Sprite, SoundGenerator, HotReloadManager

class MyGame(GameEngine):
    def initialize(self):
        # Initialize sound system
        self.sound_generator = SoundGenerator()
        self.sound_generator.initialize_default_sounds()
        
        # Setup hot-reload for development (optional)
        self.hot_reload = HotReloadManager(self)
        self.hot_reload.watch_file("game_logic.py")  # Watch specific files
        
        # Create a game object
        player = GameObject("Player")
        player.transform.position = Vector2(400, 300)
        
        # Add a sprite component
        sprite = Sprite(color='#0096FF', size=Vector2(50, 50))
        player.add_component(sprite)
        
        # Add to scene
        self.current_scene.add_object(player)
    
    def update(self, delta_time):
        # Update hot-reload system
        if hasattr(self, 'hot_reload'):
            self.hot_reload.update()
        
        # Game logic here
        if self.input_manager.is_key_pressed('space'):
            self.sound_generator.play_sound("bullet")
            print("Space pressed!")

# Run the game
game = MyGame("My 2D Game", (800, 600))
game.run()
```

## 🎯 Example Games

### Basic Example Game
Run the included example game to see the engine in action:

```bash
python example_game.py
```

### Complete UI Game
Experience a full-featured game with multiple scenes, UI elements, and particle effects:

```bash
python ui_game.py
```

### ECS Architecture Demo
See the Entity Component System in action:

```bash
python example_ecs_demo.py
```

### Logging System Demo
Explore the logging system capabilities:

```bash
python example_logging_demo.py
```

### Hot-Reload Development Demo
Experience live script reloading during development:

```bash
python example_hot_reload_demo.py
```

### Asteroids Game (1980s Arcade Classic)
Experience a complete retro game implementation:

```bash
python asteroids_game.py
```

#### Controls:
- **Left/Right or A/D**: Rotate ship
- **Up or W**: Thrust
- **Space or Ctrl**: Shoot
- **ESC**: Quit game

#### Features:
- Classic triangular ship with realistic physics
- Asteroids that split when shot
- Screen wrapping mechanics
- Wave progression system
- Procedural sound effects (bullets, explosions, engine thrust)
- Score and lives system

The examples demonstrate:
- Player movement with keyboard input
- Rotating enemies and physics simulation
- Real-time FPS display
- Component-based architecture
- Transform hierarchies
- **Procedural audio generation**
- Complete game state management

## 🔧 Architecture Overview

### Component System
The engine uses a component-based architecture where game objects are containers for components that define behavior:

```python
# Create a game object
player = GameObject("Player")

# Add components
player.add_component(Sprite(color='#FF0000'))
player.add_component(CustomBehavior())

# Components can access the game object
class CustomBehavior(Component):
    def update(self, delta_time):
        # Move the game object
        self.game_object.transform.translate(Vector2(100 * delta_time, 0))
```

### Transform Hierarchy
Supports parent-child relationships with automatic world space calculations:

```python
parent = GameObject("Parent")
child = GameObject("Child")

# Set up hierarchy
child.transform.parent = parent.transform

# Child position is relative to parent
child.transform.position = Vector2(50, 0)  # 50 units to the right of parent

# Optional 3D support
child.transform.enable_3d()
child.transform.quaternion_rotation = Quaternion.from_axis_angle(Vector3.up(), math.pi/4)
```

### Pure Python Rendering
Custom 2D renderer built on tkinter Canvas:

```python
# The renderer can draw various shapes
renderer.draw_rectangle(position, size, color='#FF0000', rotation=math.pi/4)
renderer.draw_circle(position, radius, color='#00FF00')
renderer.draw_polygon(points, color='#0000FF')
```

## 🎨 Advanced Features

### Custom Components
Extend the Component class to create custom behaviors:

```python
class HealthComponent(Component):
    def __init__(self, max_health=100):
        super().__init__()
        self.max_health = max_health
        self.current_health = max_health
    
    def take_damage(self, damage):
        self.current_health = max(0, self.current_health - damage)
        if self.current_health == 0:
            self.game_object.destroy()
```

### Input Handling
Comprehensive input system with multiple access patterns:

```python
# In your game update loop
if input_manager.is_key_just_pressed('space'):
    player.jump()

# Get normalized movement vector
movement = input_manager.get_movement_vector()
player.transform.translate(movement * speed * delta_time)
```

### Vector Mathematics
Rich 2D and 3D vector systems with all standard operations:

```python
# 2D Vector operations
velocity = Vector2(100, 50)
acceleration = Vector2(0, -9.8)
velocity += acceleration * delta_time

# 3D Vector operations
position_3d = Vector3(10, 20, 30)
direction_3d = Vector3.forward()
cross_product = position_3d.cross(direction_3d)

# Advanced operations
distance = player_pos.distance_to(enemy_pos)
direction = (target_pos - current_pos).normalize()
rotated = velocity.rotate(math.pi / 4)
```

### Procedural Audio System
Generate sound effects using mathematical waveforms:

```python
from engine import SoundGenerator

# Initialize sound system
sound_gen = SoundGenerator()

# Create custom sounds
bullet_sound = sound_gen.create_bullet_sound()
explosion_sound = sound_gen.create_explosion_sound()
engine_sound = sound_gen.create_engine_sound()

# Register and play sounds
sound_gen.register_sound(bullet_sound)
sound_gen.play_sound("bullet")

# Or use built-in sounds
sound_gen.initialize_default_sounds()
sound_gen.play_sound("explosion")
```

### ECS (Entity Component System)
Build games using pure ECS architecture:

```python
from engine import (
    World, Entity,
    TransformComponent, VelocityComponent, SpriteComponent,
    MovementSystem, RenderSystem
)

# Create ECS world
world = World()

# Add systems
world.add_system(MovementSystem())
world.add_system(RenderSystem(renderer))

# Create entity with components
player = world.create_entity("player")
world.add_component(player, TransformComponent(Vector2(400, 300)))
world.add_component(player, VelocityComponent(Vector2(100, 0)))
world.add_component(player, SpriteComponent('#0096FF', Vector2(50, 50)))

# Update world each frame
world.update(delta_time)
```

### Logging System
Built-in logging with multiple levels and performance monitoring:

```python
from engine import Logger

# Get logger instance
logger = Logger.get_instance()

# Configure logging
logger.set_level(Logger.Level.INFO)
logger.enable_file_logging("game.log")

# Log messages
logger.debug("Debug information")
logger.info("Game started")
logger.warning("Low health warning")
logger.error("Failed to load asset")

# Performance logging
logger.log_performance_stats(fps, frame_time, object_count)
```

### Hot-Reload System
Live script reloading for rapid development iteration:

```python
from engine import HotReloadManager

# Setup hot-reload in your game
hot_reload = HotReloadManager(game_engine)

# Watch specific files
hot_reload.watch_file("player_controller.py")
hot_reload.watch_file("enemy_ai.py")
hot_reload.watch_directory("scripts/")

# In your game loop
def update(self, delta_time):
    # Check for file changes and reload
    self.hot_reload.update()
    
    # Your game logic here...
```

### Scene Management
Organize your game into scenes for different states:

```python
menu_scene = Scene("Menu")
game_scene = Scene("Game")

# Switch between scenes
engine.load_scene(game_scene)
```

## 🎯 Why Pure Python?

This project demonstrates several important concepts:

1. **Understanding Fundamentals**: Building from scratch teaches you how game engines actually work
2. **No Dependencies**: Eliminates external library conflicts and licensing concerns
3. **Educational Value**: Perfect for learning game development concepts
4. **Portability**: Runs anywhere Python runs, no additional installations
5. **Customization**: Complete control over every aspect of the engine

## 🚀 Performance Considerations

While this engine prioritizes education and simplicity over raw performance, it includes several optimizations:

- **Efficient Vector Operations**: Optimized mathematical operations
- **Object Pooling**: Reuse game objects to reduce garbage collection
- **Spatial Partitioning**: Scene management optimized for large numbers of objects
- **Frame Rate Control**: Consistent timing regardless of system performance

## 🎓 Learning Outcomes

By studying this engine, you'll learn:

- Game engine architecture and design patterns
- 2D and 3D mathematics and coordinate systems
- Vector mathematics and quaternion rotations
- Component-based entity systems
- **Entity Component System (ECS) architecture**
- Input handling and event processing
- 2D graphics rendering techniques
- Transform hierarchies and world/local space conversions
- Scene management and state machines
- **Procedural audio generation and waveform synthesis**
- **Mathematical sound effect creation**
- **Logging and debugging systems**
- **Performance monitoring and optimization**
- **Data-oriented design patterns**
- **Hot-reload and live development workflows**
- **File system monitoring and script reloading**
- Performance optimization techniques

## 🤝 Contributing

This project is designed for educational purposes. Contributions that improve the learning experience or add well-documented features are welcome!

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using only Python's standard library**