from arango.graph import Graph

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from arango.collection import EdgeCollection
from arango.typings import Json

class BaseEdgeUseCases:
    def __init__(self, db_client: ArangoDBClient, graph: Graph,vertex_names:dict) -> None:
        self._db_client = db_client
        self._graph = graph
        self.vertex_names = vertex_names
        for key, value in self.vertex_names.items():
            self._db_client.create_edge_collection(self._graph,str(key),value["from"], value["to"])
        self.edge_collection_names = None

    def get_all_entities(self, name)-> EdgeCollection | None:
        if self._graph.has_edge_collection(name):
            return self._graph.edge_collection(name)
        return None

    def create_new_entity(self, edge_data:Json, name:str)-> bool | Json:
        return self._db_client.add_edge(self._graph, name, edge_data)

    def get_entity(self, entity_id: str, name) -> Json | None:
        return self._graph.edge_collection(name).get(entity_id)

    def delete_entity(self, entity_id: str, name)->Json|None:
        return self._graph.edge_collection(name).delete(entity_id)

