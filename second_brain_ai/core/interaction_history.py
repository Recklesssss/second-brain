from datetime import datetime
from core.memory_system import MemoryStorageService
from core.logging.logger import LoggerFactory


class InteractionHistoryService:
    """
    Tracks conversations and interactions between user and AI.
    """

    def __init__(self):
        self.logger = LoggerFactory.create_logger("interaction_history")
        self.memory = MemoryStorageService()

    def create_session(self, user_id: str, session_id: str):
        """
        Create a session for a user.
        """
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat()
        }

        session_node = self.memory.store_memory("Session", session_data)

        self.memory.link_memory(
            "User",
            user_id,
            "Session",
            session_id,
            "HAS_SESSION"
        )

        return session_node

    def record_interaction(self, session_id: str, interaction_id: str):
        """
        Record a new interaction inside a session.
        """
        interaction_data = {
            "interaction_id": interaction_id,
            "created_at": datetime.utcnow().isoformat()
        }

        interaction_node = self.memory.store_memory("Interaction", interaction_data)

        self.memory.link_memory(
            "Session",
            session_id,
            "Interaction",
            interaction_id,
            "HAS_INTERACTION"
        )

        return interaction_node

    def store_message(self, interaction_id: str, role: str, content: str):
        """
        Store a message inside an interaction.
        """
        message_data = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }

        message_node = self.memory.store_memory("Message", message_data)

        self.memory.link_memory(
            "Interaction",
            interaction_id,
            "Message",
            message_data.get("timestamp"),
            "HAS_MESSAGE"
        )

        return message_node

    def get_session_history(self, session_id: str):
        """
        Retrieve conversation history for a session.
        """
        query = """
        MATCH (s:Session {session_id: $session_id})-[:HAS_INTERACTION]->(i)
        OPTIONAL MATCH (i)-[:HAS_MESSAGE]->(m)
        RETURN s, i, m
        """

        return self.memory.search_memory(query, {"session_id": session_id})