"""Schema loader package.

Provides access to the schema registry loader.
"""

from .schema_loader import SchemaRegistryLoader, get_schema_registry

__all__ = [
    "SchemaRegistryLoader",
    "get_schema_registry",
]
