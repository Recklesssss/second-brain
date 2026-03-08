from datetime import datetime
from core.knowledge_graph import KnowledgeGraphService
from core.logging.logger import LoggerFactory


class MemoryStorageService:
    """
    Persistent AI memory storage system.
    """

    def __init__(self):
        self.logger = LoggerFactory.create_logger("memory_system")
        self.graph = KnowledgeGraphService()

    def store_memory(self, label: str, properties: dict):
        """
        Store a memory node in the knowledge graph.
        """
        properties["created_at"] = datetime.utcnow().isoformat()

        result = self.graph.create_node(label, properties)

        self.logger.info(f"Memory stored: {label}")

        return result

    def get_memory_by_id(self, label: str, memory_id: str):
        """
        Retrieve memory by ID.
        """
        return self.graph.get_node_by_id(label, memory_id)

    def link_memory(self, from_label, from_id, to_label, to_id, relationship):
        """
        Create relationship between memories.
        """
        return self.graph.create_relationship(
            from_label,
            from_id,
            to_label,
            to_id,
            relationship
        )

    def search_memory(self, cypher_query: str, parameters: dict = None):
        """
        Perform memory search queries.
        """
        return self.graph.query(cypher_query, parameters or {})