from fastapi import FastAPI
import uvicorn

from gighunt.modules.application import Application
from gighunt.modules.controller import Controller

app = FastAPI()
application = Application(app)
controller = Controller(application)
app.include_router(controller.router)


def start_backend():
    uvicorn.run(
        "gighunt.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False,
    )


if __name__ == "__main__":
    start_backend()
