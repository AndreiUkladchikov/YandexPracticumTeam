from http import HTTPStatus

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
    movie_id: str, like_service: LikeService = Depends(get_like_service)
) -> Likes:
    res = await like_service.get_likes(movie_id)
    return res


@router.get(
    "/rating",
    response_model=AverageRating,
    summary="Average rating",
    description="Viewing the average user rating of a movie",
)
async def average_rating(
    movie_id: str, like_service: LikeService = Depends(get_like_service)
) -> AverageRating:
    return AverageRating()


@router.post(
    "/add_rating",
    summary="Add rating",
    description="Add user rating of a movie",
)
async def add_rating(
    movie_id: str,
    user_id: str,
    rating: Rating = Query(description="Like: 10, dislike: 0"),
    like_service: LikeService = Depends(get_like_service),
):
    await like_service.put_like(movie_id, user_id, rating)

    return HTTPStatus.OK


@router.delete(
    "/delete_rating",
    summary="Delete rating",
    description="Delete user rating of a movie",
)
async def delete_rating(
    movie_id: str,
    user_id: str,
    like_service: LikeService = Depends(get_like_service),
):
    return HTTPStatus.OK


@router.patch(
    "/change_rating",
    summary="Change rating",
    description="Change user rating of a movie",
)
async def change_rating(
    movie_id: str,
    user_id: str,
    rating: Rating,
    like_service: LikeService = Depends(get_like_service),
):
    return HTTPStatus.OK
