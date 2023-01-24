from http import HTTPStatus

from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from spectree import Response

import messages
from db_models import Role, User, UserRole
from documentation import spec
from forms import RoleForm, UserRoleForm
from helpers import check_path
from messages import ResponseForm, RoleRecord, RolesResponseForm
from services import role_service, user_role_service, user_service

roles_blueprint = Blueprint("roles", __name__)


# Update or Create
@roles_blueprint.route("/update-role", methods=["POST"])
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["Roles"]
)
@jwt_required()
def update_role(json: RoleForm):
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED
    else:
        result = user_role_service.get_permissions_of(user)
        if check_path(result["permissions"], "update-role"):
            return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    if json.id is None:
        role_service.insert(
            Role(
                name=json.name,
                permissions=json.permissions,
                access_level=json.access_level,
            )
        )
        msg = messages.success_create_role
    else:
        role = role_service.get({"id": json.id})
        role_service.update(role, json.__dict__)
        msg = messages.success_update_role

    return ResponseForm(msg=msg)


# Delete
@roles_blueprint.route("/delete-role", methods=["POST"])
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["Roles"]
)
@jwt_required()
def delete_role(json: RoleForm):
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED
    else:
        result = user_role_service.get_permissions_of(user)
        if check_path(result["permissions"], "delete-role"):
            return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    role = role_service.get({"id": json.id})
    role_service.delete(role)

    return ResponseForm(msg=messages.success_delete_role)


@roles_blueprint.route("/get-all-roles", methods=["GET"])
@spec.validate(
    resp=Response(HTTP_200=RolesResponseForm, HTTP_401=ResponseForm), tags=["Roles"]
)
@jwt_required()
def get_all_roles():
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED
    else:
        result = user_role_service.get_permissions_of(user)
        if check_path(result["permissions"], "get-all-roles"):
            return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    result = role_service.all()
    roles = [RoleRecord(**s.__dict__) for s in result]
    return RolesResponseForm(msg=messages.roles_response, records=roles)


@roles_blueprint.route("/update-user-role", methods=["POST"])
@spec.validate(
    resp=Response(HTTP_200=ResponseForm, HTTP_401=ResponseForm), tags=["Roles"]
)
@jwt_required()
def update_user_role(json: UserRoleForm):
    current_user = get_jwt_identity()
    user: User = user_service.get({"email": current_user})

    if not user:
        return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED
    else:
        result = user_role_service.get_permissions_of(user)
        if "update-role" not in result["permissions"]:
            return ResponseForm(msg=messages.bad_token), HTTPStatus.UNAUTHORIZED

    if json.id is None:
        role_service.insert(UserRole(user_id=json.user_id, role_id=json.role_id))
    else:
        role = role_service.get({"id": json.id})
        role_service.update(role, json.__dict__)

    return ResponseForm(msg=messages.success_update_user_role)
