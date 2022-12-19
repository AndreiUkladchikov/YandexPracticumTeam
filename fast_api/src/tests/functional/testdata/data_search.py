import uuid
test_data_films = [
    {
        "id": str(uuid.uuid4()),
        "type": "movie",
        "imdb_rating": 9.9,
        "genre": ["Action", "Sci-Fi"],
        "genres": [
            {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
            {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
        ],
        "title": "Test film",
        "description": "New World",
        "directors": [{"id": "123", "full_name": "Stan"}],
        "director": "Stan",
        "actors_names": ["Ann", "Bob"],
        "writers_names": ["Ben", "Howard"],
        "actors": [
            {"id": "111", "full_name": "Ann"},
            {"id": "222", "full_name": "Bob"},
        ],
        "writers": [
            {"id": "333", "full_name": "Ben"},
            {"id": "444", "full_name": "Howard"},
        ],
    }
    for _ in range(50)
]

test_genres = [
    {
        "id": "3d8d44f5-0d90-4353-88ba-4wer5d2c07ff",
        "name": "Music"
    },
    {
        "id": "opodddd5-0d90-1253-88ba-4porad2c07m1",
        "name": "Adventure"
    },
    {
        "id": "6c112345-c7ed-ddff-9184-00rwfdd9f26e",
        "name": "Action"
    }
]


