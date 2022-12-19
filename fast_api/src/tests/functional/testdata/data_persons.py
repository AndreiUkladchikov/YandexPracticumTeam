test_persons = [
    {
       "actor_in": [],
       "director_in": [],
       "full_name": "Kenneth Biller",
       "id": "264e7c46-e658-4725-8cc3-21c02c9a0721",
       "writer_in": [
          "d38bced9-f39d-47b5-ad4c-5052d76c0246"
       ]
    },
    {
       "actor_in": [],
       "director_in": [],
       "full_name": "Joe Lo Truglio",
       "id": "12ad8c57-60c3-4b4a-b776-5cd657c30789",
       "writer_in": [
          "a166f73e-944b-4815-b252-3ac6d47635e1"
       ]
    },
    {
       "actor_in": ["a166f73e-944b-4815-b252-3ac6d47635e1"],
       "director_in": [],
       "full_name": "Makenzie Moss",
       "id": "097b78cb-8dda-4f80-a450-252229987085",
       "writer_in": []
    }
]

test_film_by_person = [
    {
        "id": "a166f73e-944b-4815-b252-3ac6d47635e1",
        "type": "movie",
        "imdb_rating": 9.9,
        "genre": ["Action", "Sci-Fi"],
        "genres": [
            {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
            {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
        ],
        "title": "Test film by person",
        "description": "New World",
        "directors": [],
        "director": "",
        "actors_names": ["Makenzie Moss"],
        "writers_names": [],
        "actors": [
            {"id": "097b78cb-8dda-4f80-a450-252229987085", "full_name": "Makenzie Moss"},
        ],
        "writers": []
    }
]
