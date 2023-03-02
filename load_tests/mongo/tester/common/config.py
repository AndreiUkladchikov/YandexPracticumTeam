from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv('../.env')


class Base(BaseSettings):

    mongo_connection_url: str = Field(
        'mongodb://127.0.0.1:27019,127.0.0.1:27020'
    )
    mongo_db_name: str = Field('ugsDB')

    mongo_collection_rate: str = Field('likesAndReviews')
    mongo_collection_watch: str = Field('watchLater')

    timeit_func_call_count: int = Field(100)

    random_film_id_count: int = Field(100)
    random_user_id_count: int = Field(100)

    max_fake_reviews_count: int = Field(100)
    max_down_votes_count: int = Field(100)
    max_up_votes_count: int = Field(100)

    class Config:
        case_sensitive = False
        env_file_encoding = 'utf-8'
        env_file = '../.env'


settings = Base()
