from typing import Any, Dict, List, Optional
from neo4j import GraphDatabase, Driver
from contextlib import contextmanager

from config.settings import get_settings
from core.logging import get_logger


logger = get_logger(__name__)


class Neo4jClient:
    """
    Neo4j database client wrapper.
    """

    def __init__(self):

        settings = get_settings()

        self.uri = settings.neo4j_uri
        self.user = settings.neo4j_user
        self.password = settings.neo4j_password

        self._driver: Optional[Driver] = None

    def connect(self) -> None:

        if self._driver is None:
            logger.info("Initializing Neo4j driver", extra={"event": "neo4j_connect"})
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
            )

    def close(self) -> None:

        if self._driver:
            self._driver.close()
            self._driver = None

    @contextmanager
    def session(self):

        if self._driver is None:
            self.connect()

        session = self._driver.session()

        try:
            yield session
        finally:
            session.close()

    def run_query(
        self,
        query: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:

        parameters = parameters or {}

        with self.session() as session:

            result = session.run(query, parameters)

            records = [record.data() for record in result]

            return records


_global_client: Optional[Neo4jClient] = None


def get_neo4j_client() -> Neo4jClient:

    global _global_client

    if _global_client is None:
        _global_client = Neo4jClient()
        _global_client.connect()

    return _global_client