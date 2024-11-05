from arango.graph import Graph

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.base_vertex_use_case import BaseVertexUseCase
from arango.collection import VertexCollection, EdgeCollection
from arango.typings import Json

class UserUseCases (BaseVertexUseCase):
    def test_operation(self) -> None:
        self._db_client.create_vertex_collection(
            self._graph, "bananas"
        )
        self._db_client.create_vertex_collection(
            self._graph, "apples"
        )
        self._db_client.create_edge_collection(
            self._graph, "mix", "bananas", "apples"
        )

        self._db_client.add_vertex(
            self._graph, "bananas", {"_key": "1", "name": "Bob"}
        )
        self._db_client.add_vertex(
            self._graph, "apples", {"_key": "1", "name": "Alice"}
        )

        self._db_client.add_edge(
            self._graph,
            "mix",
            {"_key": "1-edge-2", "_from": "bananas/1", "_to": "apples/1"},
        )

        print(list(self._db_client.get_vertex_collection(self._graph, "bananas").all()))
        print(list(self._db_client.get_vertex_collection(self._graph, "apples").all()))
        print(list(self._db_client.get_edge_collection(self._graph, "mix").all()))

