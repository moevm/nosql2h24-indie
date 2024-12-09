from arango.graph import Graph

import datetime
import time
from collections import Counter

from fastapi import Response

from gighunt.modules.models import Group


from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.base_vertex_use_cases import BaseVertexUseCases
from gighunt.modules.models import GroupAnnouncement, Star, UserAnnouncement, Comment, UpdateGroup

class GroupUseCases(BaseVertexUseCases):

    def get_groups(self, page: int, page_size: int, filters: dict) -> Response:
        cursor = self.get_all_entities().all(skip=(page - 1) * page_size, limit=page_size)
        deque = cursor.batch()
        group_list = []
        star_use_cases = self.edge_use_cases.stars_use_cases
        while len(deque):
            group = deque.pop()
            star_cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOGROUP.value).find(
                {"_to": str(group["_id"])})
            stars = list(star_cursor.batch())
            group_list.append({"group": group, "stars": stars})
        return group_list

    def get_group(self, group_id: int) -> Response:
        group = self.get_entity(str(group_id))
        star_use_cases = self.edge_use_cases.stars_use_cases
        stars = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOUSER.value).find(
            {"_to": str("Group/" + str(group_id))})
        stars_count = len(stars)
        user_group_use_cases = self.edge_use_cases.user_group_use_cases
        user_groups = user_group_use_cases.get_all_entities(
            user_group_use_cases.edge_collection_names.USERGROUP.value).find(
            {"_to": str("Group/" + str(group_id))}
        ).batch()
        users = []
        for user_group_edge in user_groups:
            current_user = self.get_another_entity(user_group_edge["_from"], "User")
            current_join_date = user_group_edge["join_date"]
            users.append({"user": current_user, "join_date": current_join_date})

        prod_announcements = self.edge_use_cases.producer_announcement_use_cases
        group_announcements = prod_announcements.get_all_entities(prod_announcements.edge_collection_names.ANNOUNCEMENTFROMGROUP.value).find(
            {"_from": str("Group/" + str(group_id))}
        ).batch()
        announcements = []
        for group_ann_edge in group_announcements:
            current_ann = self.get_another_entity(group_ann_edge["_to"], "Announcement")
            current_stars = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOANNOUNCEMENT.value).find({"_to": group_ann_edge["_to"]})
            current_ann_stars_count = len(current_stars)
            announcements.append({"announcement": current_ann, "stars": current_ann_stars_count})

        group = {
            "group": group,
            "stars": stars_count,
            "participants": users,
            "announcements": announcements
        }
        return group

    def add_group(self, group: Group) -> Response:
        db_group = {
            "name":group.name,
            "creation_date": str(datetime.datetime.now().date()),
            "last_edit_date":str(datetime.datetime.now().date()),
            "avatar_uri":"",
            "genres": []
        }
        return self.create_new_entity(db_group)

    def add_star(self, star: Star) -> Response:
        star_use_case = self.edge_use_cases.stars_use_cases
        if self.get_is_group_star(star.From, star.to):
            star = star_use_case.get_all_entities(star_use_case.edge_collection_names.STARSTOGROUP.value).find({"_from":"User/" + str(star.From), "_to": "Group/" + str(star.to)}).batch().pop()
            return star_use_case.delete_entity(star["_id"], star_use_case.edge_collection_names.STARSTOGROUP.value)
        else:
            db_star = {
                "_from": "User/" + str(star.From),
                "_to": "Group/" + str(star.to)
            }
            return star_use_case.create_new_entity(db_star,star_use_case.edge_collection_names.STARSTOGROUP.value)

    def get_is_group_star(self, source_user_id: int, dest_group_id: int) ->Response:
        star_use_cases = self.edge_use_cases.stars_use_cases
        cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOGROUP.value).find({"_from": str("User/"+str(source_user_id)), "_to":str("Group/" + str(dest_group_id))})
        star = cursor.batch()
        return len(star)!=0

    def join_to_group(self, group_id: int, user_id: int):
        db_user_group = {
            "_from": "User/" + str(user_id),
            "_to": "Group/" + str(group_id),
            "join_date": str(datetime.datetime.now().date())
        }
        user_group_use_cases = self.edge_use_cases.user_group_use_cases
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

    def update_group(self, update_group: UpdateGroup):
        try:
            group = self._graph.vertex_collection(self._name).update(
                {"_key": str(update_group.id), "name": update_group.name,
                 "avatar_uri": update_group.photo})
            return {
                "code": 200,
                "status": "success update",
                "user": group
            }
        except Exception as err:
            return {
                "code": 500,
                "status": "something wrong: " + str(err),
                "user": self.get_entity(str("User/" + str(update_group.id)))
            }
        return

    def get_popular_group(self) -> Response:
        try:
            star_use_cases = self.edge_use_cases.stars_use_cases
            stars = star_use_cases.get_all_entities(
                star_use_cases.edge_collection_names.STARSTOGROUP.value).all().batch()
            group_id = [star["_to"] for star in stars]
            counter = Counter(group_id)
            popular_group_id = counter.most_common(1)[0][0]

            popular_stars = star_use_cases.get_all_entities(
                star_use_cases.edge_collection_names.STARSTOGROUP.value).find(
                {"_to": str(popular_group_id)})
            stars_count = len(popular_stars)

            user_group_use_cases = self.edge_use_cases.user_group_use_cases
            user_groups = user_group_use_cases.get_all_entities(
                user_group_use_cases.edge_collection_names.USERGROUP.value).find(
                {"_to": str(popular_group_id)}
            ).batch()
            user_groups_count = len(user_groups)

            group = {
                "group": self.get_entity(popular_group_id),
                "stars": stars_count,
                "participants": user_groups_count
            }
            return {
                "status": 200,
                "message": "success",
                "group": group
            }
        except IndexError as err:
            return {
                "status": 400,
                "message": "groups doesnt have stars!",
                "group": None
            }

    def get_all_stars(self):
        star_use_cases = self.edge_use_cases.stars_use_cases
        stars = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOGROUP.value).all().batch()
        stars_count = len(stars)
        return stars_count
