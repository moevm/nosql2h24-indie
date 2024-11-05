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
        client = ArangoClient(hosts='http://arangodb:8529')

        arangodb_client = ArangoDBClient(client)
        arangodb_client.delete_database("test-db")

        arangodb_client.create_database("test-db")
        database = arangodb_client.connect_to_database("test-db")
        graph = arangodb_client.create_graph_in_database(database, "test-graph")

        self._announcement_use_cases = AnnouncementUseCases(arangodb_client, graph)
        self._group_use_cases = GroupUseCases(arangodb_client, graph)
        self._user_use_cases = UserUseCases(arangodb_client, graph)
        self._place_use_cases = PlaceUseCases(arangodb_client, graph)

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
