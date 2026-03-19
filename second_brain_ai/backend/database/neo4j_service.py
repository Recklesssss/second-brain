import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime

class MockNeo4jService:
    """Mock implementation of Neo4j graph database for development."""
    def __init__(self):
        self.nodes = {}  # node_id -> dict
        self.edges = []  # dict of relationships
        self._seed_data()

    def _seed_data(self):
        # 1. Domains
        d_cs = self.create_node(["Domain"], {"name": "Computer Science", "description": "Study of algorithms, data structures and computation"})
        d_math = self.create_node(["Domain"], {"name": "Mathematics", "description": "Study of numbers, quantities, and shapes"})

        # 2. Concepts
        c_algo = self.create_node(["Concept"], {"name": "Algorithms"})
        c_ds = self.create_node(["Concept"], {"name": "Data Structures"})
        c_graph = self.create_node(["Concept"], {"name": "Graph Theory"})

        # Relationships: Concept belongs to Domain
        self.create_relationship(c_algo["id"], d_cs["id"], "BELONGS_TO")
        self.create_relationship(c_ds["id"], d_cs["id"], "BELONGS_TO")
        self.create_relationship(c_graph["id"], d_math["id"], "BELONGS_TO")
        self.create_relationship(c_graph["id"], d_cs["id"], "BELONGS_TO")

        # Relationships: Dependencies
        self.create_relationship(c_algo["id"], c_ds["id"], "DEPENDS_ON")

        # 3. User & Personalization
        u_test = self.create_node(["User"], {"id": "user_1", "name": "Test User"})
        self.create_relationship(u_test["id"], c_ds["id"], "KNOWS", {"mastery_level": 0.9})
        self.create_relationship(u_test["id"], c_algo["id"], "NEEDS_TO_LEARN")
        self.create_relationship(u_test["id"], c_graph["id"], "NEEDS_TO_LEARN")

        # 4. Resources
        r_clrs = self.create_node(["Resource"], {"title": "Introduction to Algorithms"})
        self.create_relationship(r_clrs["id"], c_algo["id"], "PROVIDES_KNOWLEDGE_ON")

        # 5. Seed Learning Path (lp1) for the user
        lp1 = self.create_node(["LearningPath"], {
            "id": "lp1",
            "title": "Foundations of Deep Learning",
            "domain": "Machine Learning",
            "user_id": "user_1",
            "progress": 68,
            "modules_count": 4,
            "estimated_time": "12 hours"
        })
        mod1 = self.create_node(["LearningModule"], {"title": "Neural Network Basics", "description": "Intro to perceptrons", "domain": "Machine Learning"})
        mod2 = self.create_node(["LearningModule"], {"title": "Backpropagation", "description": "Chain rule and gradients", "domain": "Machine Learning"})
        self.create_relationship(lp1["id"], mod1["id"], "HAS_MODULE")
        self.create_relationship(lp1["id"], mod2["id"], "HAS_MODULE")

    def create_node(self, labels: List[str], properties: Dict[str, Any]):
        node_id = properties.get("id", str(uuid.uuid4()))
        properties["id"] = node_id
        properties.setdefault("created_at", datetime.utcnow().isoformat())
        node = {"id": node_id, "labels": labels, "properties": properties}
        self.nodes[node_id] = node
        return properties

    def create_relationship(self, source_id: str, target_id: str, rel_type: str, properties: Dict[str, Any] = None):
        edge = {
            "source": source_id,
            "target": target_id,
            "type": rel_type,
            "properties": properties or {}
        }
        self.edges.append(edge)
        return edge

    # Query methods
    def get_nodes_by_label(self, label: str):
        return [n["properties"] for n in self.nodes.values() if label in n["labels"]]
        
    def get_node(self, node_id: str):
        node = self.nodes.get(node_id)
        return node["properties"] if node else None

    def get_learning_path(self, user_id: str):
        """Returns all learning paths for a user."""
        paths = self.get_nodes_by_label("LearningPath")
        # Filter by user_id if provided
        return [p for p in paths if p.get("user_id") == user_id]

    def get_modules_for_path(self, path_id: str):
        """Returns modules linked to a path via HAS_MODULE."""
        module_ids = [e["target"] for e in self.edges if e["source"] == path_id and e["type"] == "HAS_MODULE"]
        return [self.get_node(mid) for mid in module_ids if self.get_node(mid)]


# Global instance for mock db
db = MockNeo4jService()
