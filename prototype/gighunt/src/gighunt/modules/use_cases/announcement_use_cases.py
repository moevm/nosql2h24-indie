from arango.graph import Graph

import datetime
import time

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.base_vertex_use_cases import BaseVertexUseCases

from fastapi import Response

from gighunt.modules.models import GroupAnnouncement, Star, UserAnnouncement, Comment

class AnnouncementUseCases(BaseVertexUseCases):

    def get_announcements(self, page: int, page_size: int, filters: dict) -> Response:
        cursor = self.get_all_entities().all(skip=(page - 1) * page_size, limit=page_size)
        deque = cursor.batch()
        announcement_list = []
        star_use_cases = self.edge_use_cases.stars_use_cases
        while len(deque):
            announcement = deque.pop()
            producer_announcements_use_case = self.edge_use_cases.producer_announcement_use_cases
            user_ann = list(producer_announcements_use_case.get_all_entities(producer_announcements_use_case.edge_collection_names.ANNOUNCEMENTFROMUSER.value).find({"_to":announcement["_id"]}).batch())
            group_ann = list(producer_announcements_use_case.get_all_entities(producer_announcements_use_case.edge_collection_names.ANNOUNCEMENTFROMGROUP.value).find({"_to":announcement["_id"]}).batch())
            prod_ann = None
            sender = {}
            if len(user_ann):
                prod_ann = user_ann[0]
                sender = self.get_another_entity(prod_ann.get("_from"), "User")
            elif len(group_ann):
                prod_ann = group_ann[0]
                sender = self.get_another_entity(prod_ann.get("_from"), "Group")
            else:
                print("no sender?")
            star_cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOANNOUNCEMENT.value).find(
                {"_to": str(announcement["_id"])})
            user_stars = {}
            stars = list(star_cursor.batch())
            announcement_list.append({"announcement": announcement, "stars": stars, "sender": sender})
        return announcement_list

    def get_comments(self, announcement_id: int) -> Response:
        cursor = self.get_all_entities().find({"_to":str("Announcement/"+str(announcement_id))})
        deque = cursor.batch()
        comment_list = []
        comment_use_case = self.edge_use_cases.comment_use_cases
        while len(deque):
            comment = deque.pop()
            user = self.get_another_entity(comment["_from"], "User")
            comment_list.append({"comment": comment, "sender": user})
        return comment_list

    def add_user_announcement(self, user_announcement: UserAnnouncement) -> Response:
        db_announcement = {
            "creation_date": str(datetime.datetime.now().date()),
            "content": user_announcement.announcement.get("content"),
            "tag": user_announcement.announcement.get("tag")
        }
        announcement = self.create_new_entity(db_announcement)
        ann_id =  announcement.get("_id")
        prod_ann_data = {
            "_from": "User/" + str(user_announcement.user_id),
            "_to": ann_id
        }
        prod_ann_use_cases = self.edge_use_cases.producer_announcement_use_cases
        prod_ann_use_cases.create_new_entity(prod_ann_data, prod_ann_use_cases.edge_collection_names.ANNOUNCEMENTFROMUSER.value)
        return announcement

    def add_comment(self, comment: Comment) -> Response:
        comment_use_case = self.edge_use_cases.comment_use_cases
        db_comment = {
            "_from": "User/" + str(comment.user_id),
            "_to": "Announcement/" + str(comment.announcement_id),
            "creation_date": str(datetime.datetime.now().date()),
            "content": comment.comment
        }
        return comment_use_case.create_new_entity(db_comment,comment_use_case.edge_collection_names.COMMENTTOANNOUNCEMENT.value)

    def add_star(self, star: Star) -> Response:
        star_use_case = self.edge_use_cases.stars_use_cases
        if (self.get_is_announcement_star(star.From, star.to)):
            star = star_use_case.get_all_entities(star_use_case.edge_collection_names.STARSTOANNOUNCEMENT.value).find({"_from":"User/" + str(star.From), "_to": "Announcement/" + str(star.to)}).batch().pop()
            return star_use_case.delete_entity(star["_id"], star_use_case.edge_collection_names.STARSTOANNOUNCEMENT.value)
        else:
            db_star = {
                "_from": "User/" + str(star.From),
                "_to": "Announcement/" +str(star.to)
            }
            return star_use_case.create_new_entity(db_star,star_use_case.edge_collection_names.STARSTOANNOUNCEMENT.value)

    def add_group_announcement(self, group_announcement: GroupAnnouncement) -> Response:
        db_announcement = {
            "creation_date": str(datetime.datetime.now().date()),
            "content": group_announcement.announcement.get("content"),
            "tag": group_announcement.announcement.get("tag")
        }
        announcement = self.create_new_entity(db_announcement)
        ann_id = announcement.get("_id")
        prod_ann_data = {
            "_from": "Group/" + str(group_announcement.group_id),
            "_to": ann_id
        }
        prod_ann_use_cases = self.edge_use_cases.producer_announcement_use_cases
        prod_ann_use_cases.create_new_entity(prod_ann_data,
                                                    prod_ann_use_cases.edge_collection_names.ANNOUNCEMENTFROMGROUP.value)
        return announcement

    def get_is_announcement_star(self, source_user_id: int, dest_announcement_id: int) ->Response:
        star_use_cases = self.edge_use_cases.stars_use_cases
        cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOANNOUNCEMENT.value).find({"_from": str("User/"+str(source_user_id)), "_to":str("Announcement/" + str(dest_announcement_id))})
        star = cursor.batch()
        return len(star)!=0

    def get_popular_announcement(self):
        try:
            star_use_cases = self.edge_use_cases.stars_use_cases
            stars = star_use_cases.get_all_entities(
                star_use_cases.edge_collection_names.STARSTOANNOUNCEMENT.value).all().batch()
            announcement_id = [star["_to"] for star in stars]
            counter = Counter(announcement_id)
            popular_announcement_id = counter.most_common(1)[0][0]
            return {
                "status": 200,
                "message": "success",
                "announcement": self.get_entity(popular_announcement_id)
            }
        except IndexError as err:
            return {
                "status": 400,
                "message": "users doesnt have stars!",
                "announcement": None
            }
        pass

