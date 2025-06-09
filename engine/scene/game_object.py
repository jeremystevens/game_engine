"""
GameObject class - the base entity in the game world
"""
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from ..math.transform import Transform
from ..math.vector2 import Vector2

if TYPE_CHECKING:
    from .scene import Scene
    from ..graphics.renderer import Renderer


class Component:
    """Base component class"""
    
    def __init__(self):
        self.game_object: Optional['GameObject'] = None
        self.is_active = True
    
    def start(self):
        """Called when the component is first added"""
        pass
    
    def update(self, delta_time: float):
        """Called every frame"""
        pass
    
    def render(self, renderer: 'Renderer'):
        """Called every frame for rendering"""
        pass
    
    def destroy(self):
        """Called when the component is destroyed"""
        pass


class GameObject:
    """Base game object class"""
    
    def __init__(self, name: str = "GameObject"):
        self.name = name
        self.is_active = True
        self.is_destroyed = False
        self.z_order = 0  # Render order (higher values render on top)
        self.tags: List[str] = []
        
        # Transform component (always present)
        self.transform = Transform()
        
        # Components
        self.components: Dict[type, Component] = {}
        self.components_list: List[Component] = []
        
        # Scene reference
        self.scene: Optional['Scene'] = None
        
        # Custom data storage
        self.data: Dict[str, Any] = {}
    
    def start(self):
        """Called when the object is first created"""
        for component in self.components_list:
            component.start()
    
    def update(self, delta_time: float):
        """Update the game object and all its components"""
        if not self.is_active or self.is_destroyed:
            return
        
        for component in self.components_list:
            if component.is_active:
                component.update(delta_time)
    
    def render(self, renderer: 'Renderer'):
        """Render the game object and all its components"""
        if not self.is_active or self.is_destroyed:
            return
        
        for component in self.components_list:
            if component.is_active:
                component.render(renderer)
    
    def add_component(self, component: Component) -> Component:
        """Add a component to the game object"""
        component_type = type(component)
        
        # Remove existing component of the same type
        if component_type in self.components:
            self.remove_component(component_type)
        
        # Add new component
        self.components[component_type] = component
        self.components_list.append(component)
        component.game_object = self
        
        # Initialize if object is already started
        if self.scene:
            component.start()
        
        return component
    
    def get_component(self, component_type: type) -> Optional[Component]:
        """Get a component of the specified type"""
        return self.components.get(component_type)
    
    def has_component(self, component_type: type) -> bool:
        """Check if the object has a component of the specified type"""
        return component_type in self.components
    
    def remove_component(self, component_type: type) -> bool:
        """Remove a component of the specified type"""
        if component_type in self.components:
            component = self.components[component_type]
            component.destroy()
            del self.components[component_type]
            self.components_list.remove(component)
            component.game_object = None
            return True
        return False
    
    def add_tag(self, tag: str):
        """Add a tag to the object"""
        if tag not in self.tags:
            self.tags.append(tag)
            
            # Update scene indices
            if self.scene:
                if tag not in self.scene.objects_by_tag:
                    self.scene.objects_by_tag[tag] = []
                self.scene.objects_by_tag[tag].append(self)
    
    def remove_tag(self, tag: str):
        """Remove a tag from the object"""
        if tag in self.tags:
            self.tags.remove(tag)
            
            # Update scene indices
            if self.scene and tag in self.scene.objects_by_tag:
                if self in self.scene.objects_by_tag[tag]:
                    self.scene.objects_by_tag[tag].remove(self)
                if not self.scene.objects_by_tag[tag]:
                    del self.scene.objects_by_tag[tag]
    
    def has_tag(self, tag: str) -> bool:
        """Check if the object has a specific tag"""
        return tag in self.tags
    
    def destroy(self):
        """Mark the object for destruction"""
        if self.is_destroyed:
            return
        
        self.is_destroyed = True
        
        # Destroy all components
        for component in self.components_list.copy():
            component.destroy()
        
        self.components.clear()
        self.components_list.clear()
    
    def set_active(self, active: bool):
        """Set the active state of the object"""
        self.is_active = active
    
    def set_position(self, position: Vector2):
        """Set the position of the object"""
        self.transform.position = position
    
    def get_position(self) -> Vector2:
        """Get the position of the object"""
        return self.transform.position
    
    def translate(self, delta: Vector2):
        """Move the object by a delta vector"""
        self.transform.translate(delta)
    
    def set_rotation(self, rotation: float):
        """Set the rotation of the object (in radians)"""
        self.transform.rotation = rotation
    
    def get_rotation(self) -> float:
        """Get the rotation of the object (in radians)"""
        return self.transform.rotation
    
    def rotate(self, delta_rotation: float):
        """Rotate the object by a delta angle (in radians)"""
        self.transform.rotate(delta_rotation)
    
    def set_scale(self, scale: Vector2):
        """Set the scale of the object"""
        self.transform.scale = scale
    
    def get_scale(self) -> Vector2:
        """Get the scale of the object"""
        return self.transform.scale
    
    def __str__(self) -> str:
        return f"GameObject(name='{self.name}', active={self.is_active}, components={len(self.components)})"