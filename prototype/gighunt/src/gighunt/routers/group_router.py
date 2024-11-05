from typing import Any

from fastapi import APIRouter

from gighunt.modules.use_cases.group_use_cases import GroupUseCases


class GroupRouter:
    def __init__(self, router: APIRouter, use_cases: GroupUseCases) -> None:
        self._router = router
        self._use_cases = use_cases

    def _get_groups(self) -> Any:
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

    def _get_group(self) -> Any:
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


    def _add_group(self) -> Any:
        """
        POST /api/group

        Response:
        {
            name: String
        }
        """
