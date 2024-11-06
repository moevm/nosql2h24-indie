# API Router documentation: https://fastapi.tiangolo.com/reference/apirouter/

from typing import Any
from fastapi import APIRouter, Response

from gighunt.modules.application import Application
from gighunt.modules.models import File
from gighunt.routers.announcement_router import AnnouncementRouter
from gighunt.routers.group_router import GroupRouter
from gighunt.routers.place_router import PlaceRouter
from gighunt.routers.user_router import UserRouter


class Controller:
    def __init__(self, application: Application) -> None:
        self._application = application
        self._router = APIRouter()
        self._user_router = UserRouter(self._router, self._application.user_use_cases)
        self._announcement_router = AnnouncementRouter(self._router, self._application.announcement_use_cases)
        self._group_router = GroupRouter(self._router, self._application.group_use_cases)
        self._place_router = PlaceRouter(self._router, self._application.place_use_cases)
        self._router.add_api_route("/", self.root, methods=["GET"])
        self._router.add_api_route("/api/import_data", self._import_data, methods=["POST"])
        self._router.add_api_route("/api/export_data", self._export_data, methods=["GET"])

    @property
    def router(self) -> APIRouter:
        return self._router

    async def root(self) -> Response:
        return {"message": "Hello, World! It's Gighunt!"}

    async def _import_data(self, file: File) -> Response:
        """
        POST /api/import_data

        Request:
        File
        """

    async def _export_data(self) -> Response:
        """
        GET /api/export_data

        Response:
        File
        """
