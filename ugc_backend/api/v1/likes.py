from http import HTTPStatus

from core.custom_log import logger
from fastapi import APIRouter, Depends, HTTPException, Query
from models.likes import AverageRating, Likes, Rating
from services.likes import LikeService, get_like_service

router = APIRouter()


@router.get(
    "",
    response_model=Likes,
    summary="Likes and dislikes",
    description="Viewing the number of likes and dislikes of a movie",
)
async def likes_view(
    film_id: str, like_service: LikeService = Depends(get_like_service)
) -> Likes:
    res = await like_service.get_likes(film_id)
    return res


@router.get(
    "/rating",
    response_model=AverageRating,
    summary="Average rating",
    description="Viewing the average user rating of a movie",
)
async def average_rating(
    film_id: str, like_service: LikeService = Depends(get_like_service)
) -> AverageRating:
    rating = await like_service.average_rating(film_id)
    return rating


@router.post(
    "/add_rating",
    summary="Add rating",
    description="Add user rating of a movie",
)
async def add_rating(
    film_id: str,
    user_id: str,
    rating: Rating = Query(description="Like: 10, dislike: 0"),
    like_service: LikeService = Depends(get_like_service),
):
    await like_service.put_like(film_id, user_id, rating)

    return HTTPStatus.OK


@router.delete(
    "/delete_rating",
    summary="Delete rating",
    description="Delete user rating of a movie",
)
async def delete_rating(
    film_id: str,
    user_id: str,
    like_service: LikeService = Depends(get_like_service),
):
    await like_service.delete_like(film_id, user_id)
    return HTTPStatus.OK
