# API Router documentation: https://fastapi.tiangolo.com/reference/apirouter/

import json
import logging
from fastapi import APIRouter, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse

from gighunt.modules.application import Application
from gighunt.routers.announcement_router import AnnouncementRouter
from gighunt.routers.group_router import GroupRouter
from gighunt.routers.place_router import PlaceRouter
from gighunt.routers.user_router import UserRouter


class Controller:
    def __init__(self, application: Application) -> None:
        self._logger = logging.getLogger(__name__)
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

    def fill_data_with_start_graph(self) -> None:
        start_graph_path = "src/gighunt/dump/start_graph.json"
        try:
            with open(start_graph_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self._set_dump(data)
        except (IOError, TypeError) as err:
            self._logger.error(f"Failed to fill with start graph: {err}")

    @property
    def router(self) -> APIRouter:
        return self._router

    async def root(self) -> Response:
        return {"message": "Hello, World! It's Gighunt!"}

    def _set_dump(self, graph_data) -> None:
        static = graph_data.get("static", [])
        vertices = graph_data.get("vertices", [])
        edges = graph_data.get("edges", [])

        # Vertices
        users = vertices["users"]
        groups = vertices["groups"]
        announcements = vertices["announcements"]
        places = vertices["places"]

        # Edges
        user_groups = edges["users"]["groups"]
        stars_to_users = edges["stars"]["users"]
        stars_to_groups = edges["stars"]["groups"]
        stars_to_announcements = edges["stars"]["announcements"]
        comments_to_announcements = edges["comments"]["announcements"]
        producer_announcements_from_users = edges["producer_announcements"]["users"]
        producer_announcements_from_groups = edges["producer_announcements"][
            "groups"
        ]

        # Clear graph
        # Static
        self._application.user_use_cases.get_static_collection().truncate()

        # Vertices
        self._application.user_use_cases.clear()
        self._application.group_use_cases.clear()
        self._application.announcement_use_cases.clear()
        self._application.place_use_cases.clear()

        # Edges
        self._application.edges_use_cases.user_group_use_cases.clear()
        self._application.edges_use_cases.stars_use_cases.clear()
        self._application.edges_use_cases.comment_use_cases.clear()
        self._application.edges_use_cases.producer_announcement_use_cases.clear()

        # Fill graph with new data
        # Static
        self._application.user_use_cases.get_static_collection().insert(static[0])

        # Vertices
        for user in users:
            self._application.user_use_cases.insert_json_vertex(user)
        for group in groups:
            self._application.group_use_cases.insert_json_vertex(group)
        for announcement in announcements:
            self._application.announcement_use_cases.insert_json_vertex(
                announcement
            )
        for place in places:
            self._application.place_use_cases.insert_json_vertex(place)

        # Edges
        for user_group in user_groups:
            self._application.edges_use_cases.user_group_use_cases.insert_json_edge(
                self._application.edges_use_cases.user_group_use_cases.edge_collection_names.USERGROUP.value,
                user_group,
            )
        for stars_to_user in stars_to_users:
            self._application.edges_use_cases.stars_use_cases.insert_json_edge(
                self._application.edges_use_cases.stars_use_cases.edge_collection_names.STARSTOUSER.value,
                stars_to_user,
            )
        for stars_to_group in stars_to_groups:
            self._application.edges_use_cases.stars_use_cases.insert_json_edge(
                self._application.edges_use_cases.stars_use_cases.edge_collection_names.STARSTOGROUP.value,
                stars_to_group,
            )
        for stars_to_announcement in stars_to_announcements:
            self._application.edges_use_cases.stars_use_cases.insert_json_edge(
                self._application.edges_use_cases.stars_use_cases.edge_collection_names.STARSTOANNOUNCEMENT.value,
                stars_to_announcement,
            )
        for comments_to_announcement in comments_to_announcements:
            self._application.edges_use_cases.comment_use_cases.insert_json_edge(
                self._application.edges_use_cases.comment_use_cases.edge_collection_names.COMMENTTOANNOUNCEMENT.value,
                comments_to_announcement,
            )
        for producer_announcements_from_user in producer_announcements_from_users:
            self._application.edges_use_cases.producer_announcement_use_cases.insert_json_edge(
                self._application.edges_use_cases.producer_announcement_use_cases.edge_collection_names.ANNOUNCEMENTFROMUSER.value,
                producer_announcements_from_user,
            )
        for producer_announcements_from_group in producer_announcements_from_groups:
            self._application.edges_use_cases.producer_announcement_use_cases.insert_json_edge(
                self._application.edges_use_cases.producer_announcement_use_cases.edge_collection_names.ANNOUNCEMENTFROMGROUP.value,
                producer_announcements_from_group,
            )

    def _get_dump(self) -> dict:
        # Static
        static = list(self._application.user_use_cases.get_static_collection().all())

        # Vertices
        users = list(self._application.user_use_cases.get_all_entities().all())
        groups = list(self._application.group_use_cases.get_all_entities().all())
        announcements = list(
            self._application.announcement_use_cases.get_all_entities().all()
        )
        places = list(self._application.place_use_cases.get_all_entities().all())

        # Edges
        users_groups = list(
            self._application.edges_use_cases.user_group_use_cases.get_all_entities(
                self._application.edges_use_cases.user_group_use_cases.edge_collection_names.USERGROUP.value
            ).all()
        )
        stars_to_users = list(
            self._application.edges_use_cases.stars_use_cases.get_all_entities(
                self._application.edges_use_cases.stars_use_cases.edge_collection_names.STARSTOUSER.value
            ).all()
        )
        stars_to_groups = list(
            self._application.edges_use_cases.stars_use_cases.get_all_entities(
                self._application.edges_use_cases.stars_use_cases.edge_collection_names.STARSTOGROUP.value
            ).all()
        )
        stars_to_announcement = list(
            self._application.edges_use_cases.stars_use_cases.get_all_entities(
                self._application.edges_use_cases.stars_use_cases.edge_collection_names.STARSTOANNOUNCEMENT.value
            ).all()
        )
        comments_to_announcements = list(
            self._application.edges_use_cases.comment_use_cases.get_all_entities(
                self._application.edges_use_cases.comment_use_cases.edge_collection_names.COMMENTTOANNOUNCEMENT.value
            ).all()
        )
        producer_announcements_from_users = list(
            self._application.edges_use_cases.producer_announcement_use_cases.get_all_entities(
                self._application.edges_use_cases.producer_announcement_use_cases.edge_collection_names.ANNOUNCEMENTFROMUSER.value
            ).all()
        )
        producer_announcements_from_groups = list(
            self._application.edges_use_cases.producer_announcement_use_cases.get_all_entities(
                self._application.edges_use_cases.producer_announcement_use_cases.edge_collection_names.ANNOUNCEMENTFROMGROUP.value
            ).all()
        )

        graph_data = {
            "static": static,
            "vertices": {
                "users": users,
                "groups": groups,
                "announcements": announcements,
                "places": places,
            },
            "edges": {
                "users": {
                    "groups": users_groups,
                },
                "stars": {
                    "users": stars_to_users,
                    "groups": stars_to_groups,
                    "announcements": stars_to_announcement,
                },
                "comments": {
                    "announcements": comments_to_announcements,
                },
                "producer_announcements": {
                    "users": producer_announcements_from_users,
                    "groups": producer_announcements_from_groups,
                },
            },
        }

        return graph_data


    async def _import_data(self, file: UploadFile) -> Response:
        """
        POST /api/import_data

        Request:
        UploadFile
        """
        if not file.filename.endswith(".json"):
            raise HTTPException(
                status_code=400, detail="A file with the extension .json is required"
            )

        try:
            file_content = await file.read()
            data = json.loads(file_content)
            self._set_dump(data)

            return {"message": "Graph imported successful!"}

        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
        except Exception as err:
            raise HTTPException(status_code=500, detail=f"Server error: {err}")

    async def _export_data(self) -> FileResponse:
        """
        GET /api/export_data

        Response:
        FileResponse
        """
        graph_data = self._get_dump()

        output_file = "src/gighunt/dump/graph.json"
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(graph_data, file, indent=4, ensure_ascii=False)

        return FileResponse(
            path=output_file,
            filename="graph.json",
            media_type="application/json"
        )
