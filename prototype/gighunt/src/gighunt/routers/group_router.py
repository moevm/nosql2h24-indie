from fastapi import APIRouter, Response

from gighunt.modules.models import Group
from gighunt.modules.use_cases.group_use_cases import GroupUseCases


class GroupRouter:
    def __init__(self, router: APIRouter, use_cases: GroupUseCases) -> None:
        self._router = router
        self._use_cases = use_cases
        self._router.add_api_route(
            "/api/groups/{page}{page_size}",
            self._get_groups,
            methods=["GET"],
            tags=["Group"],
        )
        self._router.add_api_route(
            "/api/group/{group_id}", self._get_group, methods=["GET"], tags=["Group"]
        )
        self._router.add_api_route(
            "/api/group", self._add_group, methods=["POST"], tags=["Group"]
        )

    def _get_groups(self, page: int, page_size: int) -> Response:
        """
        GET /api/groups?page=<pageNumber>&page_size=<pageSize>

        Response:
        [
            {
                group: Group,
                start: stars
            },
            ...
        ]
        """

    def _get_group(self, group_id: int) -> Response:
        """
        GET /api/group?group_id=<groupId>

        Response:
        {
            group: Group,
            stars: Number,
            participants: [
                {
                    user: User,
                    join_date: Date
                },
                ...
            ],
            announcements: [
                {
                    announcement: Announcement,
                    stars: Number
                },
                ...
            ]
        }
        """

    def _add_group(self, group: Group) -> Response:
        """
        POST /api/group

        Request:
        {
            name: String
        }
        """
