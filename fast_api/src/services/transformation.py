from api.models.models import PersonExtended, PersonRole
from models.person import PersonDetailed


def person_transformation(person_from_db: PersonDetailed) -> PersonExtended:
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

    return PersonExtended(id=person_from_db.id, full_name=person_from_db.full_name,
                          role=person_roles, film_ids=film_ids)
