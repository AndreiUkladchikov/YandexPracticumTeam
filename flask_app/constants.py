from db_models import Role

# Роли - access level с шагом 10
# При появлении новой роли (например Subscriber+) будет проще добавить в текущую реализацию

ROLE_USER = Role(
    name="user",
    permissions=["api/v1/films", "api/v1/genres"],
    access_level=0
)

ROLE_SUBSCRIBER = Role(
    name="subscriber",
    permissions=["api/v1/films", "api/v1/genres", "api/v1/persons"],
    access_level=10
)

ROLE_ADMIN = Role(
    name="admin",
    permissions=["api/v1/films", "api/v1/genres", "api/v1/persons", "/admin"],
    access_level=100
)

ROLE_OWNER = Role(
    name="owner",
    permissions=["api/v1/films", "api/v1/genres", "api/v1/persons", "/admin"],
    access_level=1000
)
