from fastapi import APIRouter, Request, Response

from gighunt.modules.use_cases.place_use_cases import PlaceUseCases


class PlaceRouter:
    def __init__(self, router: APIRouter, use_cases: PlaceUseCases) -> None:
        self._router = router
        self._use_cases = use_cases
        self._router.add_api_route("/api/places/{page}{page_size}", self._get_places, methods=["GET"], tags=["Place"])
        self._router.add_api_route("/api/place", self._add_place, methods=["POST"], tags=["Place"])

    def _get_places(self, page: int, page_size: int) -> Response:
        """
        GET /api/places?page=<pageNumber>&page_size=<pageSize>

        Response:
        [
            Place,
            ...
        ]
        """

    def _add_place(self, request: Request) -> Response:
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
