
"""
World class that manages the entire ECS
"""
from typing import List, Type, Optional
from .entity import Entity, EntityManager
from .component import Component
from .system import System, SystemManager


class World:
    """ECS World that manages entities, components, and systems"""
    
    def __init__(self):
        self.entity_manager = EntityManager()
        self.system_manager = SystemManager()
        self.delta_time = 0.0
        self.total_time = 0.0
    
    # Entity methods
    def create_entity(self, entity_id: str = None) -> Entity:
        """Create a new entity"""
        return self.entity_manager.create_entity(entity_id)
    
    def destroy_entity(self, entity: Entity):
        """Destroy an entity"""
        self.entity_manager.destroy_entity(entity)
    
    def get_all_entities(self) -> List[Entity]:
        """Get all entities"""
        return self.entity_manager.get_all_entities()
    
    # Component methods
    def add_component(self, entity: Entity, component: Component) -> Component:
        """Add a component to an entity"""
        return self.entity_manager.add_component(entity, component)
    
    def get_component(self, entity: Entity, component_type: Type) -> Optional[Component]:
        """Get a component from an entity"""
        return self.entity_manager.get_component(entity, component_type)
    
    def has_component(self, entity: Entity, component_type: Type) -> bool:
        """Check if entity has a component"""
        return self.entity_manager.has_component(entity, component_type)
    
    def remove_component(self, entity: Entity, component_type: Type) -> bool:
        """Remove a component from an entity"""
        return self.entity_manager.remove_component(entity, component_type)
    
    def get_entities_with_component(self, component_type: Type) -> List[Entity]:
        """Get all entities with a specific component"""
        return self.entity_manager.get_entities_with_component(component_type)
    
    def get_entities_with_components(self, *component_types: Type) -> List[Entity]:
        """Get all entities with all specified components"""
        return self.entity_manager.get_entities_with_components(*component_types)
    
    # System methods
    def add_system(self, system: System):
        """Add a system"""
        system.world = self
        self.system_manager.add_system(system)
    
    def get_system(self, system_type: Type) -> Optional[System]:
        """Get a system by type"""
        return self.system_manager.get_system(system_type)
    
    def remove_system(self, system_type: Type) -> bool:
        """Remove a system"""
        return self.system_manager.remove_system(system_type)
    
    # Update
    def update(self, delta_time: float):
        """Update the world"""
        self.delta_time = delta_time
        self.total_time += delta_time
        self.system_manager.update(delta_time)
    
    def clear(self):
        """Clear all entities and systems"""
        # Clear systems first
        self.system_manager.clear()
        
        # Clear all entities
        for entity in self.get_all_entities():
            self.destroy_entity(entity)
