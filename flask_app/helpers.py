import secrets
import string

from loguru import logger
from sqlalchemy.exc import IntegrityError

import constants
from db_models import UserRole
from services import role_service, user_role_service, user_service


def check_path(permission: list[str], url_path: str) -> bool:
    for p in permission:
        if url_path.startswith(p):
            return True
    return False


def create_test_roles():
    try:
        role_service.insert(constants.ROLE_USER)
        role_service.insert(constants.ROLE_SUBSCRIBER)
        role_service.insert(constants.ROLE_ADMIN)
        role_service.insert(constants.ROLE_OWNER)
    except IntegrityError as e:
        logger.info("Roles have been already created")


def create_test_admin():
    try:
        user_service.insert(constants.TEST_ADMIN)
        user = user_service.get({"email": constants.TEST_ADMIN.email})
        role = role_service.get({"access_level": 100})
        user_role_service.insert(UserRole(user_id=user.id, role_id=role.id))
    except IntegrityError as e:
        logger.info("Admin has been already created")


def grant_test_admin_role():
    try:
        user = user_service.get({"email": constants.TEST_ADMIN.email})
        role = role_service.get({"access_level": 100})
        user_role_service.insert(UserRole(user_id=user.id, role_id=role.id))
    except IntegrityError as e:
        logger.info("Admin already has access", e)


def generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(10))
    return password
