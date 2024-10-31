from arango import ArangoClient
from arango.collection import VertexCollection, EdgeCollection
from arango.database import StandardDatabase
from arango.graph import Graph


class ArangoDBClient:
    def __init__(self, client: ArangoClient) -> None:
        self._client = client

        self.__username = "root"
        self.__password = "password"
        self.__system_database = self._client.db(
            "_system", username=self.__username, password=self.__password
        )

    def create_database(self, database_name: str) -> None:
        if not self.__system_database.has_database(database_name):
            self.__system_database.create_database(database_name)

    def connect_to_database(self, database_name: str) -> StandardDatabase:
        return self._client.db(
            database_name, username=self.__username, password=self.__password
        )

    def create_graph_in_database(
        self, database: StandardDatabase, graph_name: str
    ) -> Graph:
        if not database.has_graph(graph_name):
            return database.create_graph(graph_name)
        return database.graph(graph_name)

    def create_vertex_collection(self, graph: Graph, collection_name: str) -> None:
        return graph.create_vertex_collection(collection_name)

    def create_edge_collection(
        self,
        graph: Graph,
        collection_name: str,
        first_vertex_collection_name: str,
        second_vertex_collection_name: str,
    ) -> None:
        return graph.create_edge_definition(
            collection_name,
            from_vertex_collections=[first_vertex_collection_name],
            to_vertex_collections=[second_vertex_collection_name],
        )

    def add_vertex(
        self, graph: Graph, vertex_collection_name: str, vertex_data: dict
    ) -> None:
        graph.insert_vertex(vertex_collection_name, vertex_data)

    def add_edge(
        self, graph: Graph, edge_collection_name: str, edge_data: dict
    ) -> None:
        graph.insert_edge(edge_collection_name, edge_data)

    def get_graph_view(self, graph: Graph, start_vertex_name: str) -> None:
        return graph.traverse(start_vertex_name)
