import datetime
import time

from fastapi import APIRouter, Response

from gighunt.modules.models import Place
from gighunt.modules.use_cases.place_use_cases import PlaceUseCases


class PlaceRouter:
    def __init__(self, router: APIRouter, use_cases: PlaceUseCases) -> None:
        self._router = router
        self._use_cases = use_cases
        self._router.add_api_route(
            "/api/places/{page}{page_size}",
            self._get_places,
            methods=["GET"],
            tags=["Place"],
        )
        self._router.add_api_route(
            "/api/place", self._add_place, methods=["POST"], tags=["Place"]
        )

    def _get_places(self, page: int, page_size: int) -> Response:
        """
        GET /api/places?page=<pageNumber>&page_size=<pageSize>

        Response:
        [
            Place,
            ...
        ]
        """
        cursor =  self._use_cases.get_all_entities().all(skip=(page-1)*page_size, limit=page_size)
        deque = cursor.batch()
        places_list = []
        while len(deque):
            place = deque.pop()
            places_list.append(place)
        return places_list

    def _add_place(self, place: Place) -> Response:
        """
        POST /api/place

        Request:
        {
            name: String,
            type: String,
            address: String,
            phone_number: String
        }
        """
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
        return self._use_cases.create_new_entity(db_place)
