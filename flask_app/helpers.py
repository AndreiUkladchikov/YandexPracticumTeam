import secrets
import string

import constants
from db_models import UserRole
from device_detector import DeviceDetector
from loguru import logger
from services import role_service, user_role_service, user_service
from sqlalchemy.exc import IntegrityError


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
    except IntegrityError:
        logger.info("Roles have been already created")


def create_test_admin():
    try:
        user_service.insert(constants.TEST_ADMIN)
        user = user_service.get({"email": constants.TEST_ADMIN.email})
        role = role_service.get({"access_level": 100})
        user_role_service.insert(UserRole(user_id=user.id, role_id=role.id))
    except IntegrityError:
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


def check_device(user_agent: str) -> str:
    dd = DeviceDetector(user_agent)
    if not dd.device_type():
        return "desktop"

    return dd.device_type()
