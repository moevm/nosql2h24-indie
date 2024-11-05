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

    announcement_use_cases = AnnouncementUseCases(arangodb_client, graph, "Announcement")
    group_use_cases = GroupUseCases(arangodb_client, graph, "Group")
    user_use_cases = UserUseCases(arangodb_client, graph, "User")

    announcement_router = AnnouncementRouter(announcement_use_cases)
    group_router = GroupRouter(group_use_cases)
    user_router = UserRouter(user_use_cases)

    user_use_cases.test_operation()
    print(user_use_cases.create_new_entity({
    "_key": "4769",
    "_id": "User/4769",
    "_rev": "_ioED4LW---",
    "first_name": "Andrey",
    "last_name": "Babenko",
    "creation_date": "2021-01-01",
    "last_edit_date": "2022-01-01",
    "avatar_uri": "assets/avatars/andrey.png",
    "talents": [
      "electric-guitar"
    ]
  }))
    print(user_use_cases.create_new_entity({
    "_key": "863",
    "_id": "User/863",
    "_rev": "_ioDTZXm---",
    "first_name": "Egor",
    "last_name": "Letov",
    "creation_date": "2021-01-01",
    "last_edit_date": "2022-01-01",
    "avatar_uri": "assets/avatars/egor.png",
    "talents": [
      "vocal",
      "acoustic-guitar",
      "electric-guitar",
      "drums"
    ]
  }))
    users = user_use_cases.get_all_entities()
    for user in users:
        print("get all users: "+ str(user))
    print("get 4769 user: "+str(user_use_cases.get_entity("4769")))
    #TODO some tests

    # uvicorn.run(
    #     "gighunt.app:app",
    #     host="0.0.0.0",
    #     port=8000,
    #     log_level="info",
    #     reload=False,
    # )


if __name__ == "__main__":
    start_backend()
