from arango.graph import Graph

import datetime
import time

from fastapi import Response
from gighunt.modules.models import Place

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.base_vertex_use_cases import BaseVertexUseCases

class PlaceUseCases(BaseVertexUseCases):

    def get_places(self, page: int, page_size: int, filters: dict) -> Response:
        cursor =  self.get_all_entities().all(skip=(page-1)*page_size, limit=page_size)
        deque = cursor.batch()
        places_list = []
        while len(deque):
            place = deque.pop()
            places_list.append(place)
        return places_list

    def add_place(self, place: Place) -> Response:
        db_place = {
                "name": place.name,
                "creation_date": str(datetime.datetime.now().date()),
                "last_edit_date": str(datetime.datetime.now().date()),
                "avatar_uri":"",
                "type": place.type,
                "address": place.address,
                "phone_number": place.phone_number,
                "area": "",
                "equipment": {"":""}
        }
        return self.create_new_entity(db_place)

    pass

