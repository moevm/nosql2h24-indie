from typing import Any
from fastapi import APIRouter

from gighunt.modules.use_cases.place_use_cases import PlaceUseCases


class PlaceRouter:
    def __init__(self, router: APIRouter, use_cases: PlaceUseCases) -> None:
        self._router = router
        self._use_cases = use_cases

    def _get_places(self) -> Any:
        """
        GET /api/places?page=<pageNumber>&page_size=<pageSize>

        Response:
        [
            Place,
            ...
        ]
        """

    def _add_place(self) -> Any:
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
