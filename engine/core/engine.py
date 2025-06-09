
"""
Core game engine class
"""
import time
import sys
from typing import Optional, Tuple, Dict, Any
from ..scene.scene import Scene
from ..input.input_manager import InputManager
from ..graphics.renderer import Renderer
from .window import Window
from .logger import Logger


class GameEngine:
    """Main game engine class that manages the game loop and core systems"""
    
    def __init__(self, title: str = "Pure Python Game Engine", size: Tuple[int, int] = (800, 600), target_fps: int = 60):
        """Initialize the game engine
        
        Args:
            title: Window title
            size: Window size as (width, height)
            target_fps: Target frames per second
        """
        self.title = title
        self.size = size
        self.target_fps = target_fps
        self.running = False
        
        # Core systems
        self.window: Optional[Window] = None
        self.renderer: Optional[Renderer] = None
        self.input_manager: Optional[InputManager] = None
        self.logger = Logger.get_instance()
        
        # Scene management
        self.current_scene: Optional[Scene] = None
        self.scenes: Dict[str, Scene] = {}
        
        # Timing
        self.last_time = 0.0
        self.delta_time = 0.0
        self.frame_count = 0
        self.fps = 0.0
        self.fps_timer = 0.0
        
        # Engine state
        self.vsync_enabled = True
        self.fullscreen = False
        
        # Initialize logger
        self.logger.info(f"Initializing {title}")
    
    def initialize(self):
        """Initialize the game - override this in your game class"""
        pass
    
    def run(self):
        """Main game loop"""
        try:
            self._initialize_systems()
            self.initialize()  # Call user initialization
            
            self.running = True
            self.last_time = time.time()
            
            self.logger.info("Starting game loop")
            
            while self.running:
                current_time = time.time()
                self.delta_time = current_time - self.last_time
                self.last_time = current_time
                
                # Update FPS counter
                self._update_fps_counter()
                
                # Handle events
                self._handle_events()
                
                # Update
                self._update()
                
                # Render
                self._render()
                
                # Frame rate limiting
                if not self.vsync_enabled:
                    self._limit_framerate()
                
                self.frame_count += 1
                
        except KeyboardInterrupt:
            self.logger.info("Game interrupted by user")
        except Exception as e:
            self.logger.error(f"Game error: {e}")
            raise
        finally:
            self._cleanup()
    
    def _initialize_systems(self):
        """Initialize core engine systems"""
        # Initialize window
        self.window = Window(self.title, self.size, self.vsync_enabled)
        
        # Initialize renderer
        self.renderer = Renderer(self.window)
        
        # Initialize input manager
        self.input_manager = InputManager(self.window)
        
        # Create default scene if none exists
        if not self.current_scene:
            self.current_scene = Scene("Default")
        
        self.logger.info("Core systems initialized")
    
    def _handle_events(self):
        """Handle window and input events"""
        if self.window:
            self.window.handle_events()
            
            # Check if window should close
            if self.window.should_close():
                self.quit()
        
        if self.input_manager:
            self.input_manager.update()
    
    def _update(self):
        """Update game logic"""
        # Update current scene
        if self.current_scene:
            self.current_scene.update(self.delta_time)
        
        # Call user update
        self.update(self.delta_time)
    
    def _render(self):
        """Render the game"""
        if self.renderer:
            self.renderer.clear()
            
            # Render current scene
            if self.current_scene:
                self.current_scene.render(self.renderer)
            
            self.renderer.present()
    
    def _update_fps_counter(self):
        """Update FPS counter"""
        self.fps_timer += self.delta_time
        if self.fps_timer >= 1.0:
            self.fps = self.frame_count / self.fps_timer
            self.frame_count = 0
            self.fps_timer = 0.0
    
    def _limit_framerate(self):
        """Limit framerate when vsync is disabled"""
        if self.target_fps > 0:
            target_frame_time = 1.0 / self.target_fps
            frame_time = time.time() - self.last_time
            
            if frame_time < target_frame_time:
                time.sleep(target_frame_time - frame_time)
    
    def _cleanup(self):
        """Cleanup resources"""
        self.logger.info("Cleaning up engine resources")
        
        if self.current_scene:
            self.current_scene.cleanup()
        
        if self.window:
            self.window.cleanup()
    
    def update(self, delta_time: float):
        """Update game logic - override this in your game class"""
        pass
    
    def quit(self):
        """Quit the game"""
        self.running = False
        self.logger.info("Game quit requested")
    
    def load_scene(self, scene: Scene):
        """Load a new scene"""
        if self.current_scene:
            self.current_scene.cleanup()
        
        self.current_scene = scene
        self.scenes[scene.name] = scene
        
        self.logger.info(f"Loaded scene: {scene.name}")
    
    def get_scene(self, name: str) -> Optional[Scene]:
        """Get a scene by name"""
        return self.scenes.get(name)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.window:
            self.fullscreen = not self.fullscreen
            self.window.set_fullscreen(self.fullscreen)
            self.logger.info(f"Fullscreen: {self.fullscreen}")
    
    def set_vsync(self, enabled: bool):
        """Enable or disable VSync"""
        self.vsync_enabled = enabled
        if self.window:
            self.window.set_vsync(enabled)
        self.logger.info(f"VSync: {enabled}")
    
    def get_fps(self) -> float:
        """Get current FPS"""
        return self.fps
    
    def get_delta_time(self) -> float:
        """Get current delta time"""
        return self.delta_time
    
    def get_frame_count(self) -> int:
        """Get total frame count"""
        return self.frame_count
    
    def set_target_fps(self, fps: int):
        """Set target FPS"""
        self.target_fps = fps
        self.logger.info(f"Target FPS set to: {fps}")
    
    def get_window_size(self) -> Tuple[int, int]:
        """Get window size"""
        return self.size
    
    def set_window_title(self, title: str):
        """Set window title"""
        self.title = title
        if self.window:
            self.window.set_title(title)
