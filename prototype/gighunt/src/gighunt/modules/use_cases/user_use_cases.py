from arango.graph import Graph

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.base_vertex_use_case import BaseVertexUseCase
from arango.collection import VertexCollection, EdgeCollection
from arango.typings import Json

class UserUseCases (BaseVertexUseCase):
    # def __init__(self, db_client: ArangoDBClient, graph: Graph, name:str) -> None:
    #     # self._db_client = db_client
    #     # self._graph = graph
    #     # self._db_client.create_vertex_collection(self._graph, "User")
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

    # def get_all_users(self)-> VertexCollection | None:
    #     return self._db_client.get_vertex_collection(self._graph, "User")
    #
    # def create_new_user(self, vertex_data:Json)->bool|Json:
    #     return self._db_client.add_vertex(self._graph, "User", vertex_data)

