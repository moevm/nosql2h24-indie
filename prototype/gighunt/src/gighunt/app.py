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
    # Подключаемся к ArangoDB
    client = ArangoClient(hosts='http://arangodb:8529')

    arangodb_client = ArangoDBClient(client)

    announcement_use_cases = AnnouncementUseCases(arangodb_client)
    group_use_cases = GroupUseCases(arangodb_client)
    user_use_cases = UserUseCases(arangodb_client)

    announcement_router = AnnouncementRouter(announcement_use_cases)
    group_router = GroupRouter(group_use_cases)
    user_router = UserRouter(user_use_cases)

    # Логинимся
    sys_db = client.db('_system', username='root', password='password')

    # Проверяем, существует ли база данных
    if not sys_db.has_database('test_db'):
        sys_db.create_database('test_db')

    # Подключаемся к базе данных
    db = client.db('test_db', username='root', password='password')

    # Проверяем, существует ли коллекция
    if not db.has_collection('test_collection'):
        collection = db.create_collection('test_collection')
    else:
        collection = db.collection('test_collection')

    # Вставляем данные
    doc = {'name': 'Alice', 'age': 25}
    collection.insert(doc)
    print('Document inserted:', doc)

    # Читаем данные
    cursor = collection.all()
    for document in cursor:
        print('Document found:', document)

    uvicorn.run(
        "gighunt.app:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )


if __name__ == "__main__":
    start_backend()
