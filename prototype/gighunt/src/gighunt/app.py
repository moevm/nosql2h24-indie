from fastapi import FastAPI
import uvicorn

from gighunt.modules.application import Application
from gighunt.modules.controller import Controller


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


def start_backend():
    application = Application(app)
    controller = Controller(application)

    application.user_use_cases.test_operation()

    # uvicorn.run(
    #     "gighunt.app:app",
    #     host="0.0.0.0",
    #     port=8000,
    #     log_level="info",
    #     reload=False,
    # )


if __name__ == "__main__":
    start_backend()
