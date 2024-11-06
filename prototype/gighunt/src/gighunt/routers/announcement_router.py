from fastapi import APIRouter, Response

from gighunt.modules.models import GroupAnnouncement, Star, UserAnnouncement, Comment
from gighunt.modules.use_cases.announcement_use_cases import AnnouncementUseCases


class AnnouncementRouter:
    def __init__(self, router: APIRouter, use_cases: AnnouncementUseCases) -> None:
        self._router = router
        self._use_cases = use_cases
        self._router.add_api_route(
            "/api/announcement/{page}{page_size}",
            self._get_announcements,
            methods=["GET"],
            tags=["Announcement"],
        )
        self._router.add_api_route(
            "/api/comments/{announcement_id}",
            self._get_comments,
            methods=["GET"],
            tags=["Announcement"],
        )
        self._router.add_api_route(
            "/api/user_announcement",
            self._add_user_announcement,
            methods=["POST"],
            tags=["Announcement"],
        )
        self._router.add_api_route(
            "/api/comment", self._add_comment, methods=["POST"], tags=["Announcement"]
        )
        self._router.add_api_route(
            "/api/star", self._add_star, methods=["POST"], tags=["Announcement"]
        )
        self._router.add_api_route(
            "/api/group_announcement",
            self._add_group_announcement,
            methods=["POST"],
            tags=["Announcement"],
        )

    def _get_announcements(self, page: int, page_size: int) -> Response:
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
        cursor = self._use_cases.get_all_entities().all(skip=(page - 1) * page_size, limit=page_size)
        deque = cursor.batch()
        announcement_list = []
        while len(deque):
            announcement = deque.pop()
            announcement_list.append({"announcement": announcement, "stars": "She was lookin kinda dumb with her finger and her thumb"})
        return announcement_list

    def _get_comments(self, announcement_id: int) -> Response:
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

    def _add_user_announcement(self, user_announcement: UserAnnouncement) -> Response:
        """
        POST /api/user_announcement

        Request:
        {
            user_id: String,
            announcement: Announcement
        }
        """

    def _add_comment(self, comment: Comment) -> Response:
        """
        POST /api/comment

        Request:
        {
            user_id: String,
            announcement_id: String,
            comment: Comment
        }
        """

    def _add_star(self, star: Star) -> Response:
        """
        POST /api/star

        {
            from: String,
            to: String
        }
        """

    def _add_group_announcement(
        self, group_announcement: GroupAnnouncement
    ) -> Response:
        """
        POST /api/group_announcement

        Request:
        {
            group_id: String,
            announcement: Announcement
        }
        """
