from __future__ import annotations

from http import HTTPStatus

from core.config import settings
from fastapi import APIRouter, Depends, HTTPException, Query
from models.likes import Rating
from models.reviews import Review
from services.reviews import ReviewService, get_review_service

router = APIRouter()


@router.get(
    "",
    response_model=list[Review],
    summary="Review to film",
    description="Add review to film",
)
async def all_reviews(
    movie_id: str,
    sort: str = Query(default="-likes", regex="^-?likes$"),
    page_number: int
    | None = Query(default=1, alias="page[number]", ge=1, le=settings.max_page_number),
    page_size: int
    | None = Query(
        default=settings.pagination_size,
        alias="page[size]",
        ge=1,
        le=settings.max_page_size,
    ),
    review_service: ReviewService = Depends(get_review_service),
) -> list[Review]:
    return list[Review]()


@router.post(
    "/add_like",
    summary="Add like/dislike",
    description="Add like or dislike to review",
)
async def add_like(
    movie_id: str,
    review_id: str,
    rating: Rating = Query(description="Like: 10, dislike: 0"),
    review_service: ReviewService = Depends(get_review_service),
):
    return HTTPStatus.OK


@router.post(
    "/add_review",
    summary="Add review",
    description="Add review to film",
)
async def add_review(
    movie_id: str,
    text: str = Query(min_length=1, max_length=7000),
    rating: Rating = Query(description="Like: 10, dislike: 0"),
    review_service: ReviewService = Depends(get_review_service),
):
    return HTTPStatus.OK
