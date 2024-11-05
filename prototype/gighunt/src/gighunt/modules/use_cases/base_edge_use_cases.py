from arango.graph import Graph

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from arango.collection import EdgeCollection
from arango.typings import Json


class BaseEdgeUseCase:
    def __init__(self, db_client: ArangoDBClient, graph: Graph, name:str) -> None:
        self._db_client = db_client
        self._graph = graph
        self._name = name
        if(not self._graph.has_edge_collection(self._name)):
            self._db_client.create_edge_collection(self._graph, name)

    def get_all_entities(self)-> EdgeCollection | None:
        if self._graph.has_edge_collection(self._name):
            return self._graph.edge_collection(self._name)
        return None

    def create_new_entity(self, edge_data:Json)-> bool | Json:
        return self._db_client.add_edge(self._graph, self._name, edge_data)

    def get_entity(self, entity_id: str) -> Json | None:
        return self._graph.edge_collection(self._name).get(entity_id)
