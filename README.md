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

### Scene System
- **Scene Management**: Organize game objects into scenes with lifecycle management
- **GameObject Architecture**: Component-based game objects with transform hierarchy
- **Component System**: Modular components for extending game object functionality
- **Object Pooling**: Efficient memory management for game objects

### Mathematics (Built from Scratch)
- **Vector2**: Comprehensive 2D vector implementation with all standard operations
- **Transform System**: Position, rotation, and scale with parent-child relationships
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

## 🏗️ Project Structure

```
engine/
├── __init__.py              # Main engine exports
├── core/
│   ├── __init__.py
│   ├── engine.py           # Main GameEngine class
│   └── window.py           # Cross-platform window management
├── scene/
│   ├── __init__.py
│   ├── scene.py            # Scene management
│   └── game_object.py      # GameObject and Component classes
├── math/
│   ├── __init__.py
│   ├── vector2.py          # 2D vector mathematics
│   └── transform.py        # Transform component
├── graphics/
│   ├── __init__.py
│   ├── renderer.py         # 2D rendering system
│   └── sprite.py           # Sprite rendering component
└── input/
    ├── __init__.py
    └── input_manager.py     # Input handling system
```

## 🚀 Installation

**No installation required!** This engine uses only Python's standard library.

Requirements:
- Python 3.7 or higher
- tkinter (included with most Python installations)

## 🎮 Quick Start

```python
from engine import GameEngine, GameObject, Vector2, Sprite

class MyGame(GameEngine):
    def initialize(self):
        # Create a game object
        player = GameObject("Player")
        player.transform.position = Vector2(400, 300)
        
        # Add a sprite component
        sprite = Sprite(color='#0096FF', size=Vector2(50, 50))
        player.add_component(sprite)
        
        # Add to scene
        self.current_scene.add_object(player)
    
    def update(self, delta_time):
        # Game logic here
        if self.input_manager.is_key_pressed('space'):
            print("Space pressed!")

# Run the game
game = MyGame("My 2D Game", (800, 600))
game.run()
```

## 🎯 Example Game

Run the included example game to see the engine in action:

```bash
python example_game.py
```

### Controls:
- **Arrow keys or WASD**: Move the blue player character
- **Q/E**: Rotate player
- **F11**: Toggle fullscreen
- **ESC**: Quit game

The example demonstrates:
- Player movement with keyboard input
- Rotating enemies moving in circular patterns
- Real-time FPS display
- Component-based architecture
- Transform hierarchies

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
Rich 2D vector system with all standard operations:

```python
# Vector operations
velocity = Vector2(100, 50)
acceleration = Vector2(0, -9.8)
velocity += acceleration * delta_time

# Advanced operations
distance = player_pos.distance_to(enemy_pos)
direction = (target_pos - current_pos).normalize()
rotated = velocity.rotate(math.pi / 4)
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
- 2D mathematics and coordinate systems
- Component-based entity systems
- Input handling and event processing
- 2D graphics rendering techniques
- Scene management and state machines
- Performance optimization techniques

## 🤝 Contributing

This project is designed for educational purposes. Contributions that improve the learning experience or add well-documented features are welcome!

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using only Python's standard library**