
"""
System and SystemManager for ECS implementation
"""
from typing import List, Dict, Type, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from .world import World


class System(ABC):
    """Base system class for ECS"""
    
    def __init__(self, priority: int = 0):
        self.priority = priority
        self.is_active = True
        self.world: Optional['World'] = None
    
    @abstractmethod
    def update(self, delta_time: float):
        """Update system logic"""
        pass
    
    def start(self):
        """Called when system is first added to world"""
        pass
    
    def stop(self):
        """Called when system is removed from world"""
        pass


class SystemManager:
    """Manages and updates systems"""
    
    def __init__(self):
        self.systems: List[System] = []
        self.systems_by_type: Dict[Type, System] = {}
    
    def add_system(self, system: System):
        """Add a system"""
        system_type = type(system)
        
        # Remove existing system of same type
        if system_type in self.systems_by_type:
            self.remove_system(system_type)
        
        # Add system
        self.systems.append(system)
        self.systems_by_type[system_type] = system
        
        # Sort by priority
        self.systems.sort(key=lambda s: s.priority)
        
        # Initialize system
        system.start()
    
    def get_system(self, system_type: Type) -> Optional[System]:
        """Get a system by type"""
        return self.systems_by_type.get(system_type)
    
    def remove_system(self, system_type: Type) -> bool:
        """Remove a system"""
        if system_type in self.systems_by_type:
            system = self.systems_by_type[system_type]
            system.stop()
            self.systems.remove(system)
            del self.systems_by_type[system_type]
            return True
        return False
    
    def update(self, delta_time: float):
        """Update all active systems"""
        for system in self.systems:
            if system.is_active:
                system.update(delta_time)
    
    def clear(self):
        """Remove all systems"""
        for system in self.systems.copy():
            system.stop()
        self.systems.clear()
        self.systems_by_type.clear()
