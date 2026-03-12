from typing import Dict, Any, List, Optional
from datetime import datetime

from database.neo4j_client import get_neo4j_client
from core.logging import get_logger


logger = get_logger(__name__)


class InteractionHistoryService:
    """
    Tracks user interactions and conversation history.
    """

    def __init__(self):
        self.client = get_neo4j_client()

    def record_interaction(
        self,
        interaction_id: str,
        user_id: str,
        message: str,
        response: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        metadata = metadata or {}

        query = """
        CREATE (i:Insight {
            id: $id,
            type: "interaction",
            user_id: $user_id,
            message: $message,
            response: $response,
            metadata: $metadata,
            created_at: $created_at
        })
        RETURN i
        """

        params = {
            "id": interaction_id,
            "user_id": user_id,
            "message": message,
            "response": response,
            "metadata": metadata,
            "created_at": datetime.utcnow().isoformat(),
        }

        result = self.client.run_query(query, params)

        return result[0] if result else {}

    def get_interaction(self, interaction_id: str) -> Optional[Dict[str, Any]]:

        query = """
        MATCH (i:Insight {id:$id, type:"interaction"})
        RETURN i
        """

        result = self.client.run_query(query, {"id": interaction_id})

        return result[0] if result else None

    def get_user_history(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:

        query = """
        MATCH (i:Insight {type:"interaction", user_id:$user_id})
        RETURN i
        ORDER BY i.created_at DESC
        LIMIT $limit
        """

        return self.client.run_query(
            query,
            {
                "user_id": user_id,
                "limit": limit,
            },
        )

    def delete_interaction(self, interaction_id: str) -> None:

        query = """
        MATCH (i:Insight {id:$id, type:"interaction"})
        DETACH DELETE i
        """

        self.client.run_query(query, {"id": interaction_id})


_global_interaction_service: Optional[InteractionHistoryService] = None


def get_interaction_service() -> InteractionHistoryService:

    global _global_interaction_service

    if _global_interaction_service is None:
        _global_interaction_service = InteractionHistoryService()

    return _global_interaction_service