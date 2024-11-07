import datetime
import time

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
        return self._use_cases.try_authorization(user_authorization)

    def _registration(self, user_registration: UserRegistration) -> Response:
        db_user = {
            "email": user_registration.email,
            "password": user_registration.password,
            "first_name": user_registration.name,
            "last_name": user_registration.surname,
            "creation_date": str(datetime.datetime.now().date()),
            "last_edit_date": str(datetime.datetime.now().date()),
            "avatar_uri": "",
            "talents": []
        }
        return self._use_cases.create_new_entity(db_user)

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
        cursor =  self._use_cases.get_all_entities().all(skip=(page-1)*page_size, limit=page_size)
        deque = cursor.batch()
        users_list = []
        star_use_cases = self._use_cases.edge_use_cases.stars_use_cases
        while len(deque):
            user = deque.pop()
            print(user["_id"])
            star_cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOUSER.value).find({"_to": str(user["_id"])})
            stars = list(star_cursor.batch())
            users_list.append({"user":user, "stars":stars})

        return users_list

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
        #TODO
        user = self._use_cases.get_entity(str(user_id))
        star_use_cases = self._use_cases.edge_use_cases.stars_use_cases
        stars = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOUSER.value).find({"_to": str("User/"+str(user_id))})
        stars_count = len(stars)
        user = {
            "user": user,
            "stars": stars_count,
            "groups": [],
            "announcements": []
        }
        return user
