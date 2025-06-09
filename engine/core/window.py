"""
Cross-platform window management using tkinter
"""
import tkinter as tk
from tkinter import Canvas
import time
from typing import Tuple, Callable, Optional
from ..math.vector2 import Vector2


class Window:
    """Cross-platform window using tkinter"""

    def __init__(self, title: str = "2D Game Engine", size: Tuple[int, int] = (800, 600)):
        self.title = title
        self.size = Vector2(size[0], size[1])
        self.is_fullscreen = False
        self._should_close = False

        # Create tkinter window
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{size[0]}x{size[1]}")
        self.root.resizable(False, False)

        # Create canvas for drawing
        self.canvas = Canvas(
            self.root,
            width=size[0],
            height=size[1],
            bg='#141928',  # Dark blue background
            highlightthickness=0
        )
        self.canvas.pack()

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Focus the window for key events
        self.root.focus_set()

        # Frame timing
        self.target_fps = 60
        self.frame_time = 1.0 / self.target_fps
        self.last_time = time.time()
        self.delta_time = 0.0
        self.actual_fps = 0.0
        self.frame_count = 0
        self.fps_timer = 0.0

        # VSync settings
        self.vsync_enabled = True
        self.frame_skip_threshold = 0.1  # Skip frame if too much time has passed

        # Event callbacks
        self.key_press_callback: Optional[Callable] = None
        self.key_release_callback: Optional[Callable] = None
        self.mouse_callback: Optional[Callable] = None

        # Bind input events
        self._setup_input_bindings()

    def _setup_input_bindings(self):
        """Setup input event bindings"""
        # Keyboard events
        self.root.bind('<KeyPress>', self._on_key_press)
        self.root.bind('<KeyRelease>', self._on_key_release)

        # Mouse events
        self.canvas.bind("<Button-1>", lambda e: self._on_mouse_click(1, e.x, e.y))
        self.canvas.bind("<Button-2>", lambda e: self._on_mouse_click(2, e.x, e.y))
        self.canvas.bind("<Button-3>", lambda e: self._on_mouse_click(3, e.x, e.y))
        self.canvas.bind("<ButtonRelease-1>", lambda e: self._on_mouse_release(1, e.x, e.y))
        self.canvas.bind("<ButtonRelease-2>", lambda e: self._on_mouse_release(2, e.x, e.y))
        self.canvas.bind("<ButtonRelease-3>", lambda e: self._on_mouse_release(3, e.x, e.y))
        self.canvas.bind("<Motion>", lambda e: self._on_mouse_move(e.x, e.y))

    def _on_key_press(self, event):
        """Handle key press events"""
        if self.key_press_callback:
            self.key_press_callback(event.keysym, event.keycode)

    def _on_key_release(self, event):
        """Handle key release events"""
        if self.key_release_callback:
            self.key_release_callback(event.keysym, event.keycode)

    def _on_mouse_click(self, button: int, x: int, y: int):
        """Handle mouse click events"""
        if self.mouse_callback:
            self.mouse_callback('click', button, x, y)

    def _on_mouse_release(self, button: int, x: int, y: int):
        """Handle mouse release events"""
        if self.mouse_callback:
            self.mouse_callback('release', button, x, y)

    def _on_mouse_move(self, x: int, y: int):
        """Handle mouse move events"""
        if self.mouse_callback:
            self.mouse_callback('move', 0, x, y)

    def set_key_press_callback(self, callback: Callable):
        """Set callback for key press events"""
        self.key_press_callback = callback

    def set_key_release_callback(self, callback: Callable):
        """Set callback for key release events"""
        self.key_release_callback = callback

    def set_mouse_callback(self, callback: Callable):
        """Set callback for mouse events"""
        self.mouse_callback = callback

    def update(self):
        """Update window and process events"""
        # Calculate delta time and FPS
        current_time = time.time()
        self.delta_time = current_time - self.last_time
        self.last_time = current_time

        # Update FPS counter
        self.frame_count += 1
        self.fps_timer += self.delta_time

        if self.fps_timer >= 1.0:
            self.actual_fps = self.frame_count / self.fps_timer
            self.frame_count = 0
            self.fps_timer = 0.0

        # Process tkinter events
        try:
            self.root.update_idletasks()
            self.root.update()
        except tk.TclError:
            self._should_close = True

        # Frame rate limiting with vsync control
        if self.vsync_enabled:
            elapsed = time.time() - current_time
            sleep_time = self.frame_time - elapsed

            # Only sleep if we have time left and it's not too long
            if sleep_time > 0 and sleep_time < self.frame_skip_threshold:
                time.sleep(sleep_time)
        else:
            # Without vsync, just process as fast as possible
            pass

    def clear(self, color: str = '#141928'):
        """Clear the canvas with specified color"""
        self.canvas.delete("all")
        self.canvas.configure(bg=color)

    def should_close(self) -> bool:
        """Check if window should close"""
        return self._should_close

    def close(self):
        """Close the window"""
        self._should_close = True

    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

    def set_title(self, title: str):
        """Set window title"""
        self.title = title
        self.root.title(title)

    def get_size(self) -> Vector2:
        """Get current window size"""
        return self.size.copy()

    def get_center(self) -> Vector2:
        """Get center point of window"""
        return Vector2(self.size.x / 2, self.size.y / 2)

    def set_vsync(self, enabled: bool):
        """Enable or disable vsync"""
        self.vsync_enabled = enabled

    def get_vsync(self) -> bool:
        """Get current vsync state"""
        return self.vsync_enabled

    def quit(self):
        """Cleanup and quit"""
        try:
            self.root.quit()
            self.root.destroy()
        except:
            pass