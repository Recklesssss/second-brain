from agents.memory_ingestion_agent import MemoryIngestionAgent


class FakeLLM:

    def generate_json(self, prompt):

        return """
        {
            "concepts":[
                {"name":"AI","description":"Artificial Intelligence"},
                {"name":"Machine Learning","description":"Subset of AI"}
            ],
            "relationships":[
                {"source":"Machine Learning","target":"AI","type":"PART_OF"}
            ]
        }
        """


class FakeGraph:

    def __init__(self):
        self.nodes = []
        self.relationships = []

    def create_node(self, label, props):
        self.nodes.append((label, props))

    def create_relationship(self, a, aid, r, b, bid):
        self.relationships.append((aid, r, bid))

    def close(self):
        pass


def test_ingestion():

    agent = MemoryIngestionAgent()

    agent.llm = FakeLLM()
    agent.graph = FakeGraph()

    result = agent.ingest_text("AI includes machine learning.")

    assert len(agent.graph.nodes) == 2