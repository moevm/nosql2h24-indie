import datetime
import time

from fastapi import APIRouter, Response

from gighunt.modules.models import Group
from gighunt.modules.use_cases.group_use_cases import GroupUseCases
from gighunt.modules.models import GroupAnnouncement, Star, UserAnnouncement, Comment

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
        self._router.add_api_route(
            "/api/group_star", self._add_star, methods=["POST"], tags=["Group"]
        )
        self._router.add_api_route(
            "/api/get_group_star",
            self._get_is_group_star,
            methods=["GET"],
            tags=["Group"]
        )
        self._router.add_api_route(
            "/api/join_to_group",
            self._join_to_group,
            methods=["POST"],
            tags=["Group"]
        )

    def _get_groups(self, page: int, page_size: int) -> Response:
        """
        GET /api/groups?page=<pageNumber>&page_size=<pageSize>

        Response:
        {[
            {
                group: Group,
                start: stars
            },
            ...
        ]}
        """
        cursor = self._use_cases.get_all_entities().all(skip=(page - 1) * page_size, limit=page_size)
        deque = cursor.batch()
        group_list = []
        star_use_cases = self._use_cases.edge_use_cases.stars_use_cases
        while len(deque):
            group = deque.pop()
            star_cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOGROUP.value).find(
                {"_to": str(group["_id"])})
            stars = list(star_cursor.batch())
            group_list.append({"group": group, "stars": stars})
        return group_list

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
        group = self._use_cases.get_entity(str(group_id))
        star_use_cases = self._use_cases.edge_use_cases.stars_use_cases
        stars = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOUSER.value).find(
            {"_to": str("Group/" + str(group_id))})
        stars_count = len(stars)
        group = {
            "group": group,
            "stars": stars_count,
            "participants": [],
            "announcements": []
        }
        return group

    def _add_group(self, group: Group) -> Response:
        """
        POST /api/group

        Request:
        {
            name: String
        }
        """
        db_group = {
            "name":group.name,
            "creation_date": str(datetime.datetime.now().date()),
            "last_edit_date":str(datetime.datetime.now().date()),
            "avatar_uri":"",
            "genres": []
        }
        return self._use_cases.create_new_entity(db_group)

    def _add_star(self, star: Star) -> Response:
        """
        POST /api/group_star

        {
            from: String,
            to: String
        }
        """
        star_use_case = self._use_cases.edge_use_cases.stars_use_cases
        if self._get_is_group_star(star.From, star.to):
            star = star_use_case.get_all_entities(star_use_case.edge_collection_names.STARSTOGROUP.value).find({"_from":"User/" + str(star.From), "_to": "Group/" + str(star.to)}).batch().pop()
            return star_use_case.delete_entity(star["_id"], star_use_case.edge_collection_names.STARSTOGROUP.value)
        else:
            db_star = {
                "_from": "User/" + str(star.From),
                "_to": "Group/" + str(star.to)
            }
            return star_use_case.create_new_entity(db_star,star_use_case.edge_collection_names.STARSTOGROUP.value)

    def _get_is_group_star(self, source_user_id: int, dest_group_id: int) ->Response:
        """
        GET /api/get_user_star?user_id=<UserId>
        :param source_user_id: int
        :param dest_group_id: int
        :return:
        Response:
        {
            value: bool
        }
        """
        star_use_cases = self._use_cases.edge_use_cases.stars_use_cases
        cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOGROUP.value).find({"_from": str("User/"+str(source_user_id)), "_to":str("Group/" + str(dest_group_id))})
        star = cursor.batch()
        return len(star)!=0

    def _join_to_group(self, group_id: int, user_id: int):
        """
        GET /api/join_to_group?group_id=<GroupId>?user_id=<UserId>
        :param group_id: int
        :param user_id: int
        :return:
        Response:
        {
            status: int,
            message: string
            UserGroup: {}
        }
        """
        db_user_group = {
            "_from": "User/" + str(user_id),
            "_to": "Group/" + str(group_id),
            "join_date": str(datetime.datetime.now().date())
        }
        user_group_use_cases = self._use_cases.edge_use_cases.user_group_use_cases
        try:
            user_group_edge = user_group_use_cases.create_new_entity(db_user_group, user_group_use_cases.edge_collection_names.USERGROUP.value)
            print(user_group_edge)
            return {
                "status": 200,
                "message": "success join to group",
                "UserGroup": user_group_edge
            }
        except Exception as err:
            print(err)
            return {
                "status": 500,
                "message": "something wrong: "+str(err),
                "UserGroup": {}
            }



