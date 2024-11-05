from fastapi import APIRouter

from gighunt.modules.application import Application
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

    def _import_data(self) -> None:
        pass

    def _export_data(self) -> None:
        pass
