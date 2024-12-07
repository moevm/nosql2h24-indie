# API Router documentation: https://fastapi.tiangolo.com/reference/apirouter/

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

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
        self._announcement_router = AnnouncementRouter(
            self._router, self._application.announcement_use_cases
        )
        self._group_router = GroupRouter(
            self._router, self._application.group_use_cases
        )
        self._place_router = PlaceRouter(
            self._router, self._application.place_use_cases
        )
        self._router.add_api_route("/", self.root, methods=["GET"])
        self._router.add_api_route(
            "/api/import_data", self._import_data, methods=["POST"]
        )
        self._router.add_api_route(
            "/api/export_data", self._export_data, methods=["GET"]
        )

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

    async def _export_data(self) -> JSONResponse:
        """
        GET /api/export_data

        Response:
        JSONResponse
        """

        # Vertices
        users = list(self._application.user_use_cases.get_all_entities().all())
        groups = list(self._application.group_use_cases.get_all_entities().all())
        announcements = list(
            self._application.announcement_use_cases.get_all_entities().all()
        )
        places = list(self._application.place_use_cases.get_all_entities().all())

        # Edges
        user_groups = list(
            self._application.edges_use_cases.user_group_use_cases.get_all_entities(
                self._application.edges_use_cases.user_group_use_cases.edge_collection_names.USERGROUP.value
            ).all()
        )
        stars_to_user = list(
            self._application.edges_use_cases.stars_use_cases.get_all_entities(
                self._application.edges_use_cases.stars_use_cases.edge_collection_names.STARSTOUSER.value
            ).all()
        )
        stars_to_group = list(
            self._application.edges_use_cases.stars_use_cases.get_all_entities(
                self._application.edges_use_cases.stars_use_cases.edge_collection_names.STARSTOGROUP.value
            ).all()
        )
        stars_to_announcement = list(
            self._application.edges_use_cases.stars_use_cases.get_all_entities(
                self._application.edges_use_cases.stars_use_cases.edge_collection_names.STARSTOANNOUNCEMENT.value
            ).all()
        )
        comments_to_announcement = list(
            self._application.edges_use_cases.comment_use_cases.get_all_entities(
                self._application.edges_use_cases.comment_use_cases.edge_collection_names.COMMENTTOANNOUNCEMENT.value
            ).all()
        )
        producer_announcements_from_user = list(
            self._application.edges_use_cases.producer_announcement_use_cases.get_all_entities(
                self._application.edges_use_cases.producer_announcement_use_cases.edge_collection_names.ANNOUNCEMENTFROMUSER.value
            ).all()
        )
        producer_announcements_from_group = list(
            self._application.edges_use_cases.producer_announcement_use_cases.get_all_entities(
                self._application.edges_use_cases.producer_announcement_use_cases.edge_collection_names.ANNOUNCEMENTFROMGROUP.value
            ).all()
        )

        graph_data = {
            "vertices": {
                "users": users,
                "groups": groups,
                "announcements": announcements,
                "places": places,
            },
            "edges": {
                "user": {
                    "groups": user_groups,
                },
                "stars": {
                    "user": stars_to_user,
                    "group": stars_to_group,
                    "announcement": stars_to_announcement,
                },
                "comments": {
                    "announcement": comments_to_announcement,
                },
                "producer_announcements": {
                    "user": producer_announcements_from_user,
                    "group": producer_announcements_from_group,
                },
            },
        }

        return graph_data
