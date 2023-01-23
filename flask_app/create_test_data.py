from loguru import logger

import constants
from clients import postgres_client
from db_models import Role, User, UserRole
from services import CustomService, UserRoleService


user_service = CustomService(client=postgres_client, model=User)
role_service = CustomService(client=postgres_client, model=Role)
user_role_service = UserRoleService(postgres_client)


def create_test_roles():
    try:
        role_service.insert(constants.ROLE_USER)
        role_service.insert(constants.ROLE_SUBSCRIBER)
        role_service.insert(constants.ROLE_ADMIN)
        role_service.insert(constants.ROLE_OWNER)
    except Exception:
        logger.info("Roles have been already created")


def create_test_admin():
    try:
        user_service.insert(constants.TEST_ADMIN)
        user = user_service.get({"email": constants.TEST_ADMIN.email})
        role = role_service.get({"access_level": 100})
        user_role_service.insert(UserRole(user_id=user.id, role_id=role.id))
    except Exception:
        logger.info("Admin has been already created")


def grant_test_admin_role():
    try:
        user = user_service.get({"email": constants.TEST_ADMIN.email})
        role = role_service.get({"access_level": 100})
        user_role_service.insert(UserRole(user_id=user.id, role_id=role.id))
    except Exception:
        logger.info("Admin already has access")
