from api.models.models import PersonDetailedInfo, PersonRole
from models.person import Person


def person_transformation(person_from_db: Person) -> PersonDetailedInfo:
    person_roles: set[PersonRole] = set()
    film_ids: set[str] = set()
    for film_id in person_from_db.actor_in:
        film_ids.add(film_id)
        person_roles.add(PersonRole.actor)

    for film_id in person_from_db.writer_in:
        film_ids.add(film_id)
        person_roles.add(PersonRole.writer)

    for film_id in person_from_db.director_in:
        film_ids.add(film_id)
        person_roles.add(PersonRole.director)

    return PersonDetailedInfo(
        roles=person_roles,
        film_ids=film_ids,
        **person_from_db.dict()
    )
