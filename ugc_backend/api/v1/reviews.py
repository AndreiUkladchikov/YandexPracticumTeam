from __future__ import annotations

from http import HTTPStatus

from api.constants.error_msg import FilmMsg, ReviewMsg
from core.config import settings
from fastapi import APIRouter, Depends, HTTPException, Query
from helpers.custom_exceptions import FilmNotFound, ReviewNotFound
from models.likes import Rating
from models.reviews import Review, ReviewResponse
from services.likes import LikeService, get_like_service
from services.reviews import ReviewService, get_review_service

router = APIRouter()


@router.get(
    "",
    response_model=list[Review],
    summary="Review to film",
    description="Add review to film",
)
async def all_reviews(
    film_id: str,
    sort: str = Query(default="-likes", regex="^-?likes$"),
    page_size: int
    | None = Query(
        default=50,
        alias="page[size]",
        ge=1,
        le=settings.max_page_size,
    ),
    review_service: ReviewService = Depends(get_review_service),
) -> list[Review] | None:
    try:
        res = await review_service.get_all_reviews(
            film_id=film_id, sort=sort, page_size=page_size
        )
    except FilmNotFound:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=FilmMsg.not_found_by_id
        )
    return res


@router.post(
    "/add_like",
    summary="Add like/dislike",
    description="Add like or dislike to review",
)
async def add_like(
    film_id: str,
    user_id: str,
    review_id: str,
    rating: Rating = Query(description="Like: 10, dislike: 0"),
    review_service: ReviewService = Depends(get_review_service),
):
    try:
        await review_service.add_like_to_review(
            film_id=film_id, user_id=user_id, review_id=review_id, rating=rating
        )
    except ReviewNotFound:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail=ReviewMsg.not_found_by_id
        )
    return HTTPStatus.OK


@router.post(
    "/add_review",
    summary="Add review",
    description="Add review to film",
    response_model=ReviewResponse,
)
async def add_review(
    film_id: str,
    user_id: str,
    text: str = Query(min_length=1, max_length=7000),
    rating: Rating = Query(description="Like: 10, dislike: 0"),
    review_service: ReviewService = Depends(get_review_service),
    like_service: LikeService = Depends(get_like_service),
) -> ReviewResponse:
    review_id: dict = await review_service.add_review(
        film_id, user_id, text, rating, like_service
    )

    return ReviewResponse(**review_id)
