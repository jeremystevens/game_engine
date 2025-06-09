
"""
Base Component class for ECS
"""
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .entity import Entity


class Component:
    """Base ECS component class"""
    
    def __init__(self):
        self.entity: Optional['Entity'] = None
        self.is_active = True
    
    def start(self):
        """Called when the component is first added to an entity"""
        pass
    
    def destroy(self):
        """Called when the component is being destroyed"""
        pass
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(entity={self.entity.id if self.entity else None})"
