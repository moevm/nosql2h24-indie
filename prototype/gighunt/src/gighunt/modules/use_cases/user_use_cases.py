from arango.graph import Graph
from fastapi import Response

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.base_vertex_use_cases import BaseVertexUseCases
from arango.collection import VertexCollection, EdgeCollection
from arango.typings import Json
from gighunt.modules.models import UserAuthorization

class UserUseCases (BaseVertexUseCases):

    def __init__(self, db_client: ArangoDBClient, graph: Graph, name:str):
        super().__init__(db_client, graph, name)
        print(super().create_new_entity({
            "email": "test@gmail.com",
            "password": "qwerty",
            "first_name": "test",
            "last_name": "user",
            "creation_date": "2021-01-01",
            "last_edit_date": "2022-01-01",
            "avatar_uri": "assets/avatars/test_user.png",
            "talents": [
                "electric-guitar"
            ]
        }))



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

    def try_authorization(self, user_authorization: UserAuthorization)->Response:
        cursor = self._graph.vertex_collection(self._name).find({"email": user_authorization.email}, limit=1)
        user_list = cursor.batch()
        print(user_list)
        if not user_list:
            return {"code": 404, "message":"user not found"}
        elif user_list[0]["password"]!= user_authorization.password:
            return {"code":401, "message":"wrong password"}
        else: return {"code":200, "message": "success authorization", "body": user_list[0]}


