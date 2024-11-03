from arango.graph import Graph

from gighunt.modules.clients.arangodb_client import ArangoDBClient


class GroupUseCases:
    def __init__(self, db_client: ArangoDBClient, graph: Graph) -> None:
        self._db_client = db_client
        self._graph = graph

