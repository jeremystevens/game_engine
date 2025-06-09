"""
Input management system for handling keyboard and mouse input
"""
from typing import Set, Dict, Tuple
from ..math.vector2 import Vector2


class InputManager:
    """Handles all input from keyboard and mouse using tkinter events"""
    
    def __init__(self):
        # Keyboard state
        self.keys_pressed: Set[str] = set()
        self.keys_just_pressed: Set[str] = set()
        self.keys_just_released: Set[str] = set()
        self.previous_keys: Set[str] = set()
        
        # Mouse state
        self.mouse_position = Vector2.zero()
        self.mouse_buttons_pressed: Set[int] = set()
        self.mouse_buttons_just_pressed: Set[int] = set()
        self.mouse_buttons_just_released: Set[int] = set()
        self.previous_mouse_buttons: Set[int] = set()
        
        # Key mapping for consistent key names
        self.key_map = {
            'Up': 'up',
            'Down': 'down', 
            'Left': 'left',
            'Right': 'right',
            'w': 'w',
            'a': 'a',
            's': 's',
            'd': 'd',
            'q': 'q',
            'e': 'e',
            'space': 'space',
            'Escape': 'escape',
            'F11': 'f11'
        }
        
        # Frame-specific input events
        self.frame_key_presses: Set[str] = set()
        self.frame_key_releases: Set[str] = set()
        self.frame_mouse_clicks: Set[int] = set()
    
    def update(self):
        """Update input state - call this once per frame"""
        # Store previous states
        self.previous_keys = self.keys_pressed.copy()
        self.previous_mouse_buttons = self.mouse_buttons_pressed.copy()
        
        # Calculate just pressed/released from frame events
        self.keys_just_pressed = self.frame_key_presses.copy()
        self.keys_just_released = self.frame_key_releases.copy()
        self.mouse_buttons_just_pressed = self.frame_mouse_clicks.copy()
        
        # Calculate just released mouse buttons
        self.mouse_buttons_just_released = self.previous_mouse_buttons - self.mouse_buttons_pressed
        
        # Clear frame-specific events
        self.frame_key_presses.clear()
        self.frame_key_releases.clear()
        self.frame_mouse_clicks.clear()
    
    def on_key_press(self, keysym: str, keycode: int):
        """Handle key press events from window"""
        key = self.key_map.get(keysym, keysym.lower())
        if key not in self.keys_pressed:
            self.keys_pressed.add(key)
            self.frame_key_presses.add(key)
    
    def on_key_release(self, keysym: str, keycode: int):
        """Handle key release events from window"""
        key = self.key_map.get(keysym, keysym.lower())
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
            self.frame_key_releases.add(key)
    
    def on_mouse_event(self, event_type: str, button: int, x: int, y: int):
        """Handle mouse events from window"""
        if event_type == 'move':
            self.mouse_position = Vector2(x, y)
        elif event_type == 'click':
            if button not in self.mouse_buttons_pressed:
                self.mouse_buttons_pressed.add(button)
                self.frame_mouse_clicks.add(button)
    
    # Keyboard methods
    def is_key_pressed(self, key: str) -> bool:
        """Check if a key is currently being held down"""
        return key.lower() in self.keys_pressed
    
    def is_key_just_pressed(self, key: str) -> bool:
        """Check if a key was just pressed this frame"""
        return key.lower() in self.keys_just_pressed
    
    def is_key_just_released(self, key: str) -> bool:
        """Check if a key was just released this frame"""
        return key.lower() in self.keys_just_released
    
    # Mouse methods
    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if a mouse button is currently being held down"""
        return button in self.mouse_buttons_pressed
    
    def is_mouse_button_just_pressed(self, button: int) -> bool:
        """Check if a mouse button was just pressed this frame"""
        return button in self.mouse_buttons_just_pressed
    
    def is_mouse_button_just_released(self, button: int) -> bool:
        """Check if a mouse button was just released this frame"""
        return button in self.mouse_buttons_just_released
    
    def get_mouse_position(self) -> Vector2:
        """Get current mouse position"""
        return self.mouse_position.copy()
    
    # Convenience methods for common keys
    def is_arrow_key_pressed(self) -> Tuple[bool, bool, bool, bool]:
        """Check arrow keys (up, down, left, right)"""
        return (
            self.is_key_pressed('up'),
            self.is_key_pressed('down'),
            self.is_key_pressed('left'),
            self.is_key_pressed('right')
        )
    
    def is_wasd_pressed(self) -> Tuple[bool, bool, bool, bool]:
        """Check WASD keys (w, a, s, d)"""
        return (
            self.is_key_pressed('w'),
            self.is_key_pressed('a'),
            self.is_key_pressed('s'),
            self.is_key_pressed('d')
        )
    
    def get_movement_vector(self) -> Vector2:
        """Get normalized movement vector from arrow keys or WASD"""
        movement = Vector2.zero()
        
        # Check arrow keys
        up, down, left, right = self.is_arrow_key_pressed()
        if up:
            movement.y -= 1
        if down:
            movement.y += 1
        if left:
            movement.x -= 1
        if right:
            movement.x += 1
        
        # If no arrow keys, check WASD
        if movement.magnitude == 0:
            w, a, s, d = self.is_wasd_pressed()
            if w:
                movement.y -= 1
            if s:
                movement.y += 1
            if a:
                movement.x -= 1
            if d:
                movement.x += 1
        
        # Normalize for diagonal movement
        if movement.magnitude > 0:
            movement = movement.normalize()
        
        return movement