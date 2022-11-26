from __future__ import annotations

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.genre import GenreService, get_genre_service

from api.v1.schema import Genre

router = APIRouter()


@router.get("/", response_model=list[Genre])
async def genre_list(
    film_service: GenreService = Depends(get_genre_service),
) -> list[Genre]:
    genres = await film_service.get_list_genres()
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return genres


@router.get("/{genre_id}", response_model=Genre)
async def genre_details(
    genre_id: str, film_service: GenreService = Depends(get_genre_service)
) -> Genre:
    genre = await film_service.get_genre_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genres not found")
    return genre
