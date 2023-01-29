import constants
from loguru import logger
from services import role_service
from sqlalchemy.exc import IntegrityError


def create_test_roles():
    try:
        role_service.insert(constants.ROLE_USER)
        role_service.insert(constants.ROLE_SUBSCRIBER)
        role_service.insert(constants.ROLE_ADMIN)
        role_service.insert(constants.ROLE_OWNER)
    except IntegrityError:
        logger.info("Roles have been already created")


create_test_roles()
