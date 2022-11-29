import unittest
import requests
from core import config


class TestGenre(unittest.TestCase):
    def setUp(self) -> None:
        settings = config.Settings()
        self.baseurl = (
            f"http://{settings.BACKEND_HOST}:{settings.BACKEND_PORT}/api/v1/genres"
        )

    def test_genre_list(self):
        response = requests.get(self.baseurl + "/")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json(),
            [
                {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
                {"id": "120a21cf-9097-479e-904a-13dd7198c1dd", "name": "Adventure"},
                {"id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd", "name": "Fantasy"},
                {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"},
                {"id": "1cacff68-643e-4ddd-8f57-84b62538081a", "name": "Drama"},
                {"id": "56b541ab-4d66-4021-8708-397762bff2d4", "name": "Music"},
                {"id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5", "name": "Romance"},
                {"id": "526769d7-df18-4661-9aa6-49ed24e9dfd8", "name": "Thriller"},
                {"id": "ca88141b-a6b4-450d-bbc3-efa940e4953f", "name": "Mystery"},
                {"id": "5373d043-3f41-4ea8-9947-4b746c601bbd", "name": "Comedy"},
                {"id": "6a0a479b-cfec-41ac-b520-41b2b007b611", "name": "Animation"},
                {"id": "55c723c1-6d90-4a04-a44b-e9792040251a", "name": "Family"},
                {"id": "ca124c76-9760-4406-bfa0-409b1e38d200", "name": "Biography"},
                {"id": "9c91a5b2-eb70-4889-8581-ebe427370edd", "name": "Musical"},
                {"id": "63c24835-34d3-4279-8d81-3c5f4ddb0cdc", "name": "Crime"},
                {"id": "a886d0ec-c3f3-4b16-b973-dedcf5bfa395", "name": "Short"},
                {"id": "0b105f87-e0a5-45dc-8ce7-f8632088f390", "name": "Western"},
                {"id": "6d141ad2-d407-4252-bda4-95590aaf062a", "name": "Documentary"},
                {"id": "eb7212a7-dd10-4552-bf7b-7a505a8c0b95", "name": "History"},
                {"id": "c020dab2-e9bd-4758-95ca-dbe363462173", "name": "War"},
                {"id": "fb58fd7f-7afd-447f-b833-e51e45e2a778", "name": "Game-Show"},
                {"id": "e508c1c8-24c0-4136-80b4-340c4befb190", "name": "Reality-TV"},
                {"id": "f39d7b6d-aef2-40b1-aaf0-cf05e7048011", "name": "Horror"},
                {"id": "2f89e116-4827-4ff4-853c-b6e058f71e31", "name": "Sport"},
                {"id": "31cabbb5-6389-45c6-9b48-f7f173f6c40f", "name": "Talk-Show"},
                {"id": "f24fd632-b1a5-4273-a835-0119bd12f829", "name": "News"},
            ],
        )

    def test_specific_genre(self):
        genre_id = "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff"
        response = requests.get(self.baseurl + f"/{genre_id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
        )


class TestPerson(unittest.TestCase):
    def setUp(self) -> None:
        settings = config.Settings()
        self.baseurl = (
            f"http://{settings.BACKEND_HOST}:{settings.BACKEND_PORT}/api/v1/persons"
        )

    def test_person_search_without_paging(self):
        query = "Phillip"
        response = requests.get(self.baseurl + f"/search?query={query}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["total"], 6)

    def test_person_search_with_paging(self):
        query = "Phillip"
        page_size = 3
        page_number = 2
        response = requests.get(
            self.baseurl
            + f"/search?query={query}&page[number]={page_number}&page[size]={page_size}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total"], 6)
        self.assertEqual(response.json()["page"], page_number)
        self.assertEqual(response.json()["size"], page_size)


    def test_specific_person(self):
        person_id = "51ab9a43-7d80-45f5-95cf-dcf9abd19980"
        response = requests.get(self.baseurl + f"/{person_id}")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                "id": "51ab9a43-7d80-45f5-95cf-dcf9abd19980",
                "full_name": "Todd Terry",
                "role": ["actor"],
                "film_ids": ["c8316f09-81ca-4b71-a879-405e740acee5"],
            },
        )

    def test_films_of_specific_person(self):
        person_id = "51ab9a43-7d80-45f5-95cf-dcf9abd19980"
        response = requests.get(self.baseurl + f"/{person_id}/film")
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response.json(),
            [
                {
                    "id": "c8316f09-81ca-4b71-a879-405e740acee5",
                    "title": "Beyond the Farthest Star",
                    "imdb_rating": 7.4,
                }
            ],
        )
