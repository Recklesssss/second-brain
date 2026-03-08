from database.neo4j_client import Neo4jClient


class KnowledgeGraph:
    """
    Core CRUD service for interacting with the Neo4j knowledge graph.
    All AI modules use this interface instead of writing raw queries.
    """

    def __init__(self):

        self.client = Neo4jClient()
        self.client.connect()

    # -----------------------------
    # Node Operations
    # -----------------------------

    def create_node(self, label: str, properties: dict):

        query = f"""
        CREATE (n:{label} $props)
        RETURN n
        """

        result = self.client.run_query(query, {"props": properties})

        return result

    def get_node(self, label: str, node_id: str):

        query = f"""
        MATCH (n:{label} {{id: $id}})
        RETURN n
        """

        result = self.client.run_query(query, {"id": node_id})

        return result[0] if result else None

    def update_node(self, label: str, node_id: str, properties: dict):

        query = f"""
        MATCH (n:{label} {{id: $id}})
        SET n += $props
        RETURN n
        """

        return self.client.run_query(query, {"id": node_id, "props": properties})

    def delete_node(self, label: str, node_id: str):

        query = f"""
        MATCH (n:{label} {{id: $id}})
        DETACH DELETE n
        """

        self.client.run_query(query, {"id": node_id})

    # -----------------------------
    # Relationship Operations
    # -----------------------------

    def create_relationship(
        self,
        from_label: str,
        from_id: str,
        relationship: str,
        to_label: str,
        to_id: str,
        properties: dict | None = None
    ):

        query = f"""
        MATCH (a:{from_label} {{id: $from_id}})
        MATCH (b:{to_label} {{id: $to_id}})
        CREATE (a)-[r:{relationship} $props]->(b)
        RETURN r
        """

        return self.client.run_query(
            query,
            {
                "from_id": from_id,
                "to_id": to_id,
                "props": properties or {}
            }
        )

    # -----------------------------
    # Query Interface
    # -----------------------------

    def query(self, cypher: str, params: dict | None = None):

        return self.client.run_query(cypher, params)

    # -----------------------------
    # Utility
    # -----------------------------

    def close(self):

        self.client.close()