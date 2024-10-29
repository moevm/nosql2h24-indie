from arango import ArangoClient


class ArangoDBClient:
    def __init__(self, client: ArangoClient) -> None:
        self._client = client

