from models.parent_model import BaseOrjsonModel


class Bookmarks(BaseOrjsonModel):
    user_id: str
    films_id: list[str]
