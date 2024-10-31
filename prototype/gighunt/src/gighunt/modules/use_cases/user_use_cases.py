from gighunt.modules.clients.arangodb_client import ArangoDBClient


class UserUseCases:
    def __init__(self, db_client: ArangoDBClient) -> None:
        self._db_client = db_client

    def test_operation(self) -> None:
        # clear db !

        self._db_client.create_database("test-db")
        database = self._db_client.connect_to_database("test-db")
        graph = self._db_client.create_graph_in_database(database, "test-graph")
        first_vertex_collection = self._db_client.create_vertex_collection(
            graph, "bananas"
        )
        second_vertex_collection = self._db_client.create_vertex_collection(
            graph, "apples"
        )
        edge_collection = self._db_client.create_edge_collection(
            graph, "mix", "bananas", "apples"
        )

        self._db_client.add_vertex(
            graph, "bananas", {"_key": "1", "name": "Bob"}
        )
        self._db_client.add_vertex(
            graph, "apples", {"_key": "1", "name": "Alice"}
        )

        self._db_client.add_edge(
            graph,
            edge_collection,
            {"_key": "1-edge-2", "_from": "bananas/1", "_to": "apples/1"},
        )

        print(self._db_client.get_graph_view(graph, "Bob"))
