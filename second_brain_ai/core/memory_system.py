from typing import Dict, Any, List, Optional
from datetime import datetime

from database.neo4j_client import get_neo4j_client
from core.logging import get_logger


logger = get_logger(__name__)


class MemoryStorageService:
    """
    Persistent memory storage for agents and system insights.
    """

    def __init__(self):
        self.client = get_neo4j_client()

    def store_memory(
        self,
        memory_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        metadata = metadata or {}

        query = """
        CREATE (m:Insight {
            id: $id,
            text: $text,
            created_at: $created_at,
            metadata: $metadata
        })
        RETURN m
        """

        params = {
            "id": memory_id,
            "text": text,
            "created_at": datetime.utcnow().isoformat(),
            "metadata": metadata,
        }

        result = self.client.run_query(query, params)

        return result[0] if result else {}

    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:

        query = """
        MATCH (m:Insight {id:$id})
        RETURN m
        """

        result = self.client.run_query(query, {"id": memory_id})

        return result[0] if result else None

    def list_memories(self, limit: int = 50) -> List[Dict[str, Any]]:

        query = """
        MATCH (m:Insight)
        RETURN m
        ORDER BY m.created_at DESC
        LIMIT $limit
        """

        return self.client.run_query(query, {"limit": limit})

    def delete_memory(self, memory_id: str) -> None:

        query = """
        MATCH (m:Insight {id:$id})
        DETACH DELETE m
        """

        self.client.run_query(query, {"id": memory_id})


_global_memory_service: Optional[MemoryStorageService] = None


def get_memory_service() -> MemoryStorageService:

    global _global_memory_service

    if _global_memory_service is None:
        _global_memory_service = MemoryStorageService()

    return _global_memory_service