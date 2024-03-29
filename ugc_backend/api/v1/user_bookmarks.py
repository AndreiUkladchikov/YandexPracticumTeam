from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from api.constants.error_msg import DuplicateFilmMsg
from helpers.custom_exceptions import DuplicateFilm
from models.user_bookmarks import Bookmarks
from services.user_bookmarks import BookmarkService, get_bookmark_service

router = APIRouter()


@router.get(
    "",
    response_model=Bookmarks,
    summary="User bookmarks",
    description="Viewing user bookmarks of the film",
)
async def bookmarks_view(
    user_id: str, like_service: BookmarkService = Depends(get_bookmark_service)
) -> Bookmarks:
    res = await like_service.all_bookmarks(user_id)
    return res


@router.post(
    "/add_bookmark",
    summary="Add bookmarks",
    description="Add user bookmarks of the film",
)
async def add_bookmark(
    user_id: str,
    film_id: str,
    like_service: BookmarkService = Depends(get_bookmark_service),
):
    try:
        await like_service.add_bookmark(user_id, film_id)
    except DuplicateFilm:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=DuplicateFilmMsg.film_duplicate
        )
    return HTTPStatus.OK


@router.delete(
    "/delete_bookmark",
    summary="Delete user film",
    description="Delete film from user bookmark",
)
async def delete_bookmark(
    user_id: str,
    film_id: str,
    like_service: BookmarkService = Depends(get_bookmark_service),
):
    await like_service.delete_bookmark(user_id, film_id)
    return HTTPStatus.OK
