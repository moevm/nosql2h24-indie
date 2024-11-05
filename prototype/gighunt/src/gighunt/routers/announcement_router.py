from fastapi import APIRouter, Request, Response

from gighunt.modules.use_cases.announcement_use_cases import AnnouncementUseCases


class AnnouncementRouter:
    def __init__(self, router: APIRouter, use_cases: AnnouncementUseCases) -> None:
        self._router = router
        self._use_cases = use_cases
        self._router.add_api_route("/api/announcement/{page}{page_size}", self._get_announcements, methods=["GET"], tags=["Announcement"])
        self._router.add_api_route("/api/comments/{announcement_id}", self._get_comments, methods=["GET"], tags=["Announcement"])
        self._router.add_api_route("/api/user_announcement", self._add_user_announcement, methods=["POST"], tags=["Announcement"])
        self._router.add_api_route("/api/comment", self._add_comment, methods=["POST"], tags=["Announcement"])
        self._router.add_api_route("/api/star", self._add_star, methods=["POST"], tags=["Announcement"])
        self._router.add_api_route("/api/group_announcement", self._add_group_announcement, methods=["POST"], tags=["Announcement"])

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

    def _add_user_announcement(self, request: Request) -> Response:
        """
        POST /api/user_announcement

        Request:
        {
            user_id: String,
            announcement: Announcement
        }
        """

    def _add_comment(self, request: Request) -> Response:
        """
        POST /api/comment

        Request:
        {
            user_id: String,
            announcement_id: String,
            comment: Comment
        }
        """

    def _add_star(self, request: Request) -> Response:
        """
        POST /api/star

        {
            from: String,
            to: String
        }
        """

    def _add_group_announcement(self, request: Request) -> Response:
        """
        POST /api/group_announcement

        Request:
        {
            group_id: String, 
            announcement: Announcement
        }
        """
