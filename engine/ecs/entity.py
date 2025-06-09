
"""
Entity and EntityManager for ECS implementation
"""
from typing import Dict, List, Set, Optional, Type, TypeVar
import uuid

T = TypeVar('T')


class Entity:
    """Simple entity class that holds a unique ID"""
    
    def __init__(self, entity_id: str = None):
        self.id = entity_id or str(uuid.uuid4())
        self.is_active = True
    
    def __str__(self) -> str:
        return f"Entity({self.id})"
    
    def __repr__(self) -> str:
        return self.__str__()


class EntityManager:
    """Manages entities and their components"""
    
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.components: Dict[str, Dict[Type, object]] = {}  # entity_id -> {component_type: component}
        self.component_index: Dict[Type, Set[str]] = {}  # component_type -> set of entity_ids
        
    def create_entity(self, entity_id: str = None) -> Entity:
        """Create a new entity"""
        entity = Entity(entity_id)
        self.entities[entity.id] = entity
        self.components[entity.id] = {}
        return entity
    
    def destroy_entity(self, entity: Entity):
        """Destroy an entity and all its components"""
        if entity.id in self.entities:
            # Remove all components
            for component_type in list(self.components[entity.id].keys()):
                self.remove_component(entity, component_type)
            
            # Remove entity
            del self.entities[entity.id]
            del self.components[entity.id]
    
    def add_component(self, entity: Entity, component: object) -> object:
        """Add a component to an entity"""
        component_type = type(component)
        
        # Remove existing component of same type
        if component_type in self.components[entity.id]:
            self.remove_component(entity, component_type)
        
        # Add component
        self.components[entity.id][component_type] = component
        
        # Update index
        if component_type not in self.component_index:
            self.component_index[component_type] = set()
        self.component_index[component_type].add(entity.id)
        
        # Set entity reference if component supports it
        if hasattr(component, 'entity'):
            component.entity = entity
            
        return component
    
    def get_component(self, entity: Entity, component_type: Type[T]) -> Optional[T]:
        """Get a component from an entity"""
        return self.components[entity.id].get(component_type)
    
    def has_component(self, entity: Entity, component_type: Type) -> bool:
        """Check if entity has a component"""
        return component_type in self.components[entity.id]
    
    def remove_component(self, entity: Entity, component_type: Type) -> bool:
        """Remove a component from an entity"""
        if component_type in self.components[entity.id]:
            component = self.components[entity.id][component_type]
            
            # Call destroy if component supports it
            if hasattr(component, 'destroy'):
                component.destroy()
            
            # Remove from entity
            del self.components[entity.id][component_type]
            
            # Update index
            if component_type in self.component_index:
                self.component_index[component_type].discard(entity.id)
                if not self.component_index[component_type]:
                    del self.component_index[component_type]
            
            return True
        return False
    
    def get_entities_with_component(self, component_type: Type) -> List[Entity]:
        """Get all entities that have a specific component"""
        entity_ids = self.component_index.get(component_type, set())
        return [self.entities[entity_id] for entity_id in entity_ids if entity_id in self.entities]
    
    def get_entities_with_components(self, *component_types: Type) -> List[Entity]:
        """Get all entities that have all specified components"""
        if not component_types:
            return list(self.entities.values())
        
        # Start with entities that have the first component type
        result_ids = self.component_index.get(component_types[0], set()).copy()
        
        # Intersect with entities that have each subsequent component type
        for component_type in component_types[1:]:
            component_ids = self.component_index.get(component_type, set())
            result_ids &= component_ids
        
        return [self.entities[entity_id] for entity_id in result_ids if entity_id in self.entities]
    
    def get_all_entities(self) -> List[Entity]:
        """Get all entities"""
        return list(self.entities.values())
