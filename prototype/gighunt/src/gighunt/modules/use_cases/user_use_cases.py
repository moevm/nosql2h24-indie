from arango.graph import Graph
from fastapi import Response

import datetime
import time
from collections import Counter

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.base_vertex_use_cases import BaseVertexUseCases
from arango.collection import VertexCollection, EdgeCollection
from arango.typings import Json

from gighunt.modules.use_cases.all_edge_use_cases import EdgeCollectionUseCases

from gighunt.modules.models import UserAuthorization, UserRegistration
from gighunt.modules.models import GroupAnnouncement, Star, UserAnnouncement, Comment

class UserUseCases (BaseVertexUseCases):

    def __init__(self, db_client: ArangoDBClient, graph: Graph, name:str, edge_use_cases:EdgeCollectionUseCases):
        super().__init__(db_client, graph, name, edge_use_cases)
        test_user = super().create_new_entity({
            "email": "test@gmail.com",
            "password": "qwerty",
            "first_name": "test",
            "last_name": "user",
            "creation_date": "2021-01-01",
            "last_edit_date": "2022-01-01",
            "avatar_uri": "assets/avatars/test_user.png",
            "talents": [
                "electric-guitar"
            ]
        })
        self.create_static_collection()



    def test_operation(self) -> None:
        self._db_client.create_vertex_collection(
            self._graph, "bananas"
        )
        self._db_client.create_vertex_collection(
            self._graph, "apples"
        )
        self._db_client.create_edge_collection(
            self._graph, "mix", "bananas", "apples"
        )

        self._db_client.add_vertex(
            self._graph, "bananas", {"_key": "1", "name": "Bob"}
        )
        self._db_client.add_vertex(
            self._graph, "apples", {"_key": "1", "name": "Alice"}
        )

        self._db_client.add_edge(
            self._graph,
            "mix",
            {"_key": "1-edge-2", "_from": "bananas/1", "_to": "apples/1"},
        )

        print(list(self._db_client.get_vertex_collection(self._graph, "bananas").all()))
        print(list(self._db_client.get_vertex_collection(self._graph, "apples").all()))
        print(list(self._db_client.get_edge_collection(self._graph, "mix").all()))

    def try_authorization(self, user_authorization: UserAuthorization)->Response:
        cursor = self._graph.vertex_collection(self._name).find({"email": user_authorization.email}, limit=1)
        user_list = cursor.batch()
        print(user_list)
        if not user_list:
            return {"code": 404, "message":"user not found"}
        elif user_list[0]["password"]!= user_authorization.password:
            return {"code":401, "message":"wrong password"}
        else: return {"code":200, "message": "success authorization", "body": user_list[0]}

    def create_static_collection(self)->VertexCollection:
        self.static_collection_name = "Static"
        self.static_collection = self._db_client.create_vertex_collection(self._graph, self.static_collection_name)
        static_data = {
            "equipment": [],
            "tags": ["Релиз", "Концерт", "Поиск участников", "Поиск группы", "Поиск места", "Предложение места", "Поболтать", "Поиск тульпы", "Поиск Волынского"],
            "talents": ["vocal", "guitar", "viola", "bass", "percussion"],
            "genres": []
        }
        self.static_data_vertex = self._db_client.add_vertex(self._graph, self.static_collection_name,static_data)

    def get_static_collection(self)->VertexCollection:
        return self._db_client.get_vertex_collection(self._graph, self.static_collection_name)

    def registration(self, user_registration: UserRegistration) -> Response:
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
        return self.create_new_entity(db_user)

    def get_users(self, page: int, page_size: int, filters: dict) -> Response:
        cursor = self.get_all_entities().all(skip=(page - 1) * page_size, limit=page_size)
        deque = cursor.batch()
        users_list = []
        star_use_cases = self.edge_use_cases.stars_use_cases
        while len(deque):
            user = deque.pop()
            print(user["_id"])
            star_cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOUSER.value).find(
                {"_to": str(user["_id"])})
            stars = list(star_cursor.batch())
            users_list.append({"user": user, "stars": stars})

        return users_list

    def get_user(self, user_id: int) -> Response:
        user = self.get_entity(str(user_id))
        star_use_cases = self.edge_use_cases.stars_use_cases
        stars = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOUSER.value).find({"_to": str("User/"+str(user_id))})
        stars_count = len(stars)

        prod_ann_use_case = self.edge_use_cases.producer_announcement_use_cases
        announcements = []
        all_prod_ann = prod_ann_use_case.get_all_entities(prod_ann_use_case.edge_collection_names.ANNOUNCEMENTFROMUSER.value)
        if(all_prod_ann):
            prod_announcements = list(all_prod_ann.find({"_from": str("User/" + str(user_id))}).batch())
            for edge in prod_announcements:
                ann = self.get_another_entity(edge["_to"], "Announcement")
                ann_stars = list(star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOANNOUNCEMENT.value).find({"_to":ann.get("_id")}))
                ann_struct = {
                    "announcement": ann,
                    "stars": len(ann_stars)
                }
                announcements.append(ann_struct)

        user_group_user_cases = self.edge_use_cases.user_group_use_cases
        user_groups =  user_group_user_cases.get_all_entities(user_group_user_cases.edge_collection_names.USERGROUP.value).find({"_from":str("User/" + str(user_id))})
        group_list = []
        for edge in user_groups:
            group = self.get_another_entity(edge["_to"], "Group")
            group_struct = {
                "group": group,
                "join_date": edge["join_date"]
            }
            group_list.append(group_struct)

        user = {
            "user": user,
            "stars": stars_count,
            "groups": group_list,
            "announcements": announcements
        }
        return user

    def get_is_user_star(self, source_user_id: int, dest_user_id: int) ->Response:
        star_use_cases = self.edge_use_cases.stars_use_cases
        cursor = star_use_cases.get_all_entities(star_use_cases.edge_collection_names.STARSTOUSER.value).find(
            {"_from": str("User/" + str(source_user_id)), "_to": str("User/" + str(dest_user_id))})
        star = cursor.batch()
        return len(star) != 0

    def add_star(self, star: Star) -> Response:
        star_use_case = self.edge_use_cases.stars_use_cases
        if (self.get_is_user_star(star.From, star.to)):
            star = star_use_case.get_all_entities(star_use_case.edge_collection_names.STARSTOUSER.value).find(
                {"_from": "User/" + str(star.From), "_to": "User/" + str(star.to)}).batch().pop()
            return star_use_case.delete_entity(star["_id"], star_use_case.edge_collection_names.STARSTOUSER.value)
        else:
            db_star = {
                "_from": "User/" + str(star.From),
                "_to": "User/" + str(star.to)
            }
            return star_use_case.create_new_entity(db_star, star_use_case.edge_collection_names.STARSTOUSER.value)

    def get_static_field(self, static_field:str)->Response:
        static = dict(self.get_static_collection())
        key = list(static.keys())[0]
        return static[key][static_field]

    def update_user(self):
        return

    def get_popular_user(self) ->Response:
        try:
            star_use_cases = self.edge_use_cases.stars_use_cases
            stars = star_use_cases.get_all_entities(
                star_use_cases.edge_collection_names.STARSTOUSER.value).all().batch()
            users_id = [star["_to"] for star in stars]
            counter = Counter(users_id)
            popular_user_id = counter.most_common(1)[0][0]
            return {
                "status": 200,
                "message": "success",
                "user": self.get_entity(popular_user_id)
            }
        except IndexError as err:
            return {
                "status": 400,
                "message": "users doesnt have stars!",
                "user": None
            }
        pass




