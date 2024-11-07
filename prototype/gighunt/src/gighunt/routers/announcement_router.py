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
        star_use_cases = self._use_cases.edge_use_cases.stars_use_cases
        while len(deque):
            announcement = deque.pop()
            print(announcement["_id"])
            star_cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOANNOUNCEMENT.value).find(
                {"_to": str(announcement["_id"])})
            user_stars = {}
            stars = list(star_cursor.batch())
            announcement_list.append({"user": announcement, "stars": stars})
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
        # cursor = self._use_cases.get_all_entities().all(skip=(page - 1) * page_size, limit=page_size)
        # deque = cursor.batch()
        # group_list = []
        # star_use_cases = self._use_cases.edge_use_cases.stars_use_cases
        # while len(deque):
        #     group = deque.pop()
        #     print(user["_id"])
        #     star_cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOGROUP.value).find(
        #         {"_to": str(group["_id"])})
        #     stars = list(star_cursor.batch())
        #     group_list.append({"group": group, "stars": stars})
        # return group_list

    def _add_user_announcement(self, user_announcement: UserAnnouncement) -> Response:
        """
        POST /api/user_announcement

        Request:
        {
            user_id: String,
            announcement: Announcement
        }
        """
        #TODO
        db_announcement = {
            "creation_date": str(datetime.datetime.now().date()),
            "content": user_announcement.announcement,
            "tag": ""
        }
        return self._use_cases.create_new_entity(db_announcement)

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
        comment_use_case = self._use_cases.edge_use_cases.comment_use_cases
        db_comment = {
            "_from": comment.user_id,
            "_to": comment.announcement_id,
            "creation_date": str(datetime.datetime.now().date()),
            "content": comment.comment
        }
        return comment_use_case.create_new_entity(db_comment,comment_use_case.edge_collection_names.COMMENTTOANNOUNCEMENT.value)

    #TODO copy this route in user router and group router (with changing star_use_case.edge_collection_names)
    def _add_star(self, star: Star) -> Response:
        """
        POST /api/star

        {
            from: String,
            to: String
        }
        """
        star_use_case = self._use_cases.edge_use_cases.stars_use_cases
        db_star = {
            "_from": star.From,
            "_to": star.to
        }
        return star_use_case.create_new_entity(db_star,star_use_case.edge_collection_names.STARSTOUSER.value)

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
        #TODO
        db_announcement = {
            "creation_date": str(datetime.datetime.now().date()),
            "content": user_announcement.announcement,
            "tag": ""
        }
        return self._use_cases.create_new_entity(db_announcement)
