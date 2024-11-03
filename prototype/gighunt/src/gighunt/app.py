from arango import ArangoClient
from fastapi import FastAPI
import uvicorn

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.announcement_use_cases import AnnouncementUseCases
from gighunt.modules.use_cases.group_use_cases import GroupUseCases
from gighunt.modules.use_cases.user_use_cases import UserUseCases
from gighunt.routers.announcement_router import AnnouncementRouter
from gighunt.routers.group_router import GroupRouter
from gighunt.routers.user_router import UserRouter


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


def start_backend():
    client = ArangoClient(hosts='http://arangodb:8529')

    arangodb_client = ArangoDBClient(client)
    arangodb_client.delete_database("test-db")

    arangodb_client.create_database("test-db")
    database = arangodb_client.connect_to_database("test-db")
    graph = arangodb_client.create_graph_in_database(database, "test-graph")

    announcement_use_cases = AnnouncementUseCases(arangodb_client)
    group_use_cases = GroupUseCases(arangodb_client)
    user_use_cases = UserUseCases(arangodb_client, graph)

    announcement_router = AnnouncementRouter(announcement_use_cases)
    group_router = GroupRouter(group_use_cases)
    user_router = UserRouter(user_use_cases)

    user_use_cases.test_operation()

    # uvicorn.run(
    #     "gighunt.app:app",
    #     host="0.0.0.0",
    #     port=8000,
    #     log_level="info",
    #     reload=False,
    # )


if __name__ == "__main__":
    start_backend()
