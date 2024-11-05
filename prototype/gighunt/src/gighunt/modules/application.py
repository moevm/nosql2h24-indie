from arango import ArangoClient
from fastapi import FastAPI

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.announcement_use_cases import AnnouncementUseCases
from gighunt.modules.use_cases.group_use_cases import GroupUseCases
from gighunt.modules.use_cases.place_use_cases import PlaceUseCases
from gighunt.modules.use_cases.user_use_cases import UserUseCases


class Application:
    def __init__(self, app: FastAPI) -> None:
        self._app = app
        self._arangodb_client = ArangoDBClient(ArangoClient(hosts='http://arangodb:8529'))

        self._arangodb_client.delete_database("test-db")
        self._arangodb_client.create_database("test-db")
        self._database = self._arangodb_client.connect_to_database("test-db")
        self._graph = self._arangodb_client.create_graph_in_database(self._database, "test-graph")

        self._announcement_use_cases = AnnouncementUseCases(self._arangodb_client, self._graph, "Announcement")
        self._group_use_cases = GroupUseCases(self._arangodb_client, self._graph, "Group")
        self._user_use_cases = UserUseCases(self._arangodb_client, self._graph, "User")
        self._place_use_cases = PlaceUseCases(self._arangodb_client, self._graph, "Place")

    @property
    def app(self) -> FastAPI:
        return self._app

    @property
    def announcement_use_cases(self) -> AnnouncementUseCases:
        return self._announcement_use_cases

    @property
    def group_use_cases(self) -> GroupUseCases:
        return self._group_use_cases

    @property
    def user_use_cases(self) -> UserUseCases:
        return self._user_use_cases

    @property
    def place_use_cases(self) -> PlaceUseCases:
        return self._place_use_cases

    @property
    def arangodb_client(self) -> ArangoDBClient:
        return self._arangodb_client

    @property
    def database(self) -> ArangoDBClient:
        return self._database

    @property
    def graph(self) -> ArangoDBClient:
        return self._graph
