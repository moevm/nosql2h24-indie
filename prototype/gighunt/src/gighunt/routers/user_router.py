from fastapi import APIRouter, Response

from gighunt.modules.models import UserAuthorization, UserRegistration
from gighunt.modules.use_cases.user_use_cases import UserUseCases


class UserRouter:
    def __init__(self, router: APIRouter, use_cases: UserUseCases) -> None:
        self._router = router
        self._use_cases = use_cases
        self._router.add_api_route(
            "/api/authorization", self._authorization, methods=["POST"], tags=["User"]
        )
        self._router.add_api_route(
            "/api/registration", self._registration, methods=["POST"], tags=["User"]
        )
        self._router.add_api_route(
            "/api/user/{user_id}", self._get_user, methods=["GET"], tags=["User"]
        )
        self._router.add_api_route(
            "/api/users/{page}{page_size}",
            self._get_users,
            methods=["GET"],
            tags=["User"],
        )

    def _authorization(self, user_authorization: UserAuthorization) -> Response:
        pass

    def _registration(self, user_registration: UserRegistration) -> Response:
        pass

    def _get_users(self, page: int, page_size: int) -> Response:
        """
        GET /api/users?page=<pageNumber>&page_size=<pageSize>

        Response:
        [
            {
                user: User,
                start: stars
            },
            ...
        ]
        """

    def _get_user(self, user_id: int) -> Response:
        """
        GET /api/user?user_id=<userId>

        Response:
        {
            user: User,
            stars: Number,
            groups: [
                {
                    group: Group,
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
