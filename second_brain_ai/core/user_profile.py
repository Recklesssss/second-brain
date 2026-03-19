from typing import Dict, Any, Optional
from datetime import datetime

from second_brain_ai.database.neo4j_client import get_neo4j_client
from second_brain_ai.core.logging.logger import get_logger


logger = get_logger(__name__)


class UserProfileService:
    """
    Manages persistent user learning profiles.
    """

    def __init__(self):
        self.client = get_neo4j_client()

    def create_profile(
        self,
        user_id: str,
        profile_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        query = """
        CREATE (u:Insight {
            id: $id,
            type: "user_profile",
            data: $data,
            created_at: $created_at
        })
        RETURN u
        """

        params = {
            "id": user_id,
            "data": profile_data,
            "created_at": datetime.utcnow().isoformat(),
        }

        result = self.client.run_query(query, params)

        return result[0] if result else {}

    def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:

        query = """
        MATCH (u:Insight {id:$id, type:"user_profile"})
        RETURN u
        """

        result = self.client.run_query(query, {"id": user_id})

        return result[0] if result else None

    def update_profile(
        self,
        user_id: str,
        updates: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:

        query = """
        MATCH (u:Insight {id:$id, type:"user_profile"})
        SET u.data += $updates
        RETURN u
        """

        result = self.client.run_query(
            query,
            {
                "id": user_id,
                "updates": updates,
            },
        )

        return result[0] if result else None

    def delete_profile(self, user_id: str):

        query = """
        MATCH (u:Insight {id:$id, type:"user_profile"})
        DETACH DELETE u
        """

        self.client.run_query(query, {"id": user_id})


_global_user_profile_service: Optional[UserProfileService] = None


def get_user_profile_service() -> UserProfileService:

    global _global_user_profile_service

    if _global_user_profile_service is None:
        _global_user_profile_service = UserProfileService()

    return _global_user_profile_service