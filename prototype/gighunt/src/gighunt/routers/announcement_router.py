from typing import Any
from fastapi import APIRouter

from gighunt.modules.use_cases.announcement_use_cases import AnnouncementUseCases


class AnnouncementRouter:
    def __init__(self, router: APIRouter, use_cases: AnnouncementUseCases) -> None:
        self._router = router
        self._use_cases = use_cases

    def _get_announcements(self) -> Any:
        """
        GET /api/announcements?page=<pageNumber>&page_size=<pageSize>

        Response:
        [
            {
                announcement: Announcement,
                start: stars
            },
            ...
        ]
        """

    def _get_comments(self) -> Any:
        """
        GET /api/comments?announcement_id=<aId>

        Response:
        [
            {
                comment: Comment,
                sender: User
            }
        ]
        """
        pass

    def _add_user_announcement(self) -> Any:
        """
        POST /api/user_announcement

        Request:
        {
            user_id: String,
            announcement: Announcement
        }
        """

    def _add_comment(self) -> Any:
        """
        POST /api/comment

        Request:
        {
            user_id: String,
            announcement_id: String,
            comment: Comment
        }
        """

    def _add_star(self) -> Any:
        """
        POST /api/star

        {
            from: String,
            to: String
        }
        """

    def _add_group_announcement(self) -> Any:
        """
        POST /api/group_announcement

        Request:
        {
            group_id: String, 
            announcement: Announcement
        }
        """
