from gighunt.modules.clients.arangodb_client import ArangoDBClient


class PlaceUseCases:
    def __init__(self, db_client: ArangoDBClient) -> None:
        self._db_client = db_client
