from arango.graph import Graph

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from arango.collection import EdgeCollection
from arango.typings import Json
from enum import Enum

class BaseEdgeUseCases:
    def __init__(self, db_client: ArangoDBClient, graph: Graph,vertex_names:dict) -> None:
        self._db_client = db_client
        self._graph = graph
        self.vertex_names = vertex_names
        for key, value in self.vertex_names.items():
            self._db_client.create_edge_collection(self._graph,key,value["from"], value["to"])
        names = vertex_names.keys()
        enum_names = map(str.upper, vertex_names.keys())
        self.edge_collection_names = Enum('EdgeCollectionNames', list(zip(enum_names, names)))

    def get_all_entities(self)-> EdgeCollection | None:
        if self._graph.has_edge_collection(self._name):
            return self._graph.edge_collection(self._name)
        return None

    def create_new_entity(self, edge_data:Json)-> bool | Json:
        return self._db_client.add_edge(self._graph, self._name, edge_data)

    def get_entity(self, entity_id: str) -> Json | None:
        return self._graph.edge_collection(self._name).get(entity_id)
