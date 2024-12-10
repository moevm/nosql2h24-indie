from arango.graph import Graph

import datetime
import time
import re

from fastapi import Response
from gighunt.modules.models import Place, FilterPlace

from gighunt.modules.clients.arangodb_client import ArangoDBClient
from gighunt.modules.use_cases.base_vertex_use_cases import BaseVertexUseCases

class PlaceUseCases(BaseVertexUseCases):

    def __create_filters(self, filters: FilterPlace)->dict:
        query_filters = {}
        if filters.name:
            query_filters["name"] = f".*{filters.name.lower()}.*"
        if filters.type:
            query_filters["type"] = f".*{filters.type.lower()}.*"
        if filters.address:
            query_filters["address"] = f".*{filters.address.lower()}.*"
        if filters.number:
            query_filters["number"] =  fr".*{re.escape(filters.number.lower())}.*"
        if filters.equipment:
            query_filters["equipment"] = f".*{filters.equipment.lower()}.*"
        return query_filters
    def __find_by_filters(self, deque, filters)->list:
        query_filters = self.__create_filters(filters)
        places = []
        while(len(deque)):
            flag = True
            place = deque.pop()
            if query_filters.get("name") and not re.match(query_filters["name"], place["name"].lower()):
                flag = False
            if query_filters.get("type") and not re.match(query_filters["type"], place["type"].lower()):
                flag = False
            if query_filters.get("address") and not re.match(query_filters["address"], place["address"].lower()):
                flag = False
            if query_filters.get("number") and not re.match(query_filters["number"], place["phone_number"].lower()):
                flag = False
            if query_filters.get("equipment") and not re.match(query_filters["equipment"], ''.join(list(place["equipment"].values())).lower()):
                flag = False
            if (flag):
                places.append(place)
        return places


    def get_places(self, page: int, page_size: int, filters: FilterPlace) -> Response:
        cursor =  self.get_all_entities().all(skip=(page-1)*page_size, limit=page_size)
        deque = cursor.batch()
        places = self.__find_by_filters(deque,filters)[(page - 1) * page_size : (page - 1) * page_size + page_size]
        places_list = []
        while len(places):
            place = places.pop()
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

