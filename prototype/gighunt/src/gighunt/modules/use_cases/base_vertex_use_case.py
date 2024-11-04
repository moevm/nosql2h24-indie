from arango.graph import Graph

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from arango.collection import VertexCollection
from arango.typings import Json


class BaseVertexUseCase:
    def __init__(self, db_client: ArangoDBClient, graph: Graph, name:str) -> None:
        self._db_client = db_client
        self._graph = graph
        self._name = name
        self._db_client.create_vertex_collection(self._graph, name)

    def get_all_entities(self)-> VertexCollection | None:
        if self._graph.has_vertex_collection(self._name):
            return self._graph.vertex_collection(self._name)
        return None

    def create_new_entity(self, vertex_data:Json)->bool|Json:
        return self._db_client.add_vertex(self._graph, self._name, vertex_data)

    def get_entity(self, entity_id: str) -> Json | None:
        aql = "FOR e IN "+ self._name+ " FILTER e.id == '"+ entity_id + "' RETURN e"
        print(aql)
        cursor = self._db_client.execute_query(aql)
        return cursor