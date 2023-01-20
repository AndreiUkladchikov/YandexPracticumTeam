from config import settings

address = f"http://{settings.auth_server_host}:{settings.auth_server_port}"
base_api_url = settings.base_api_url

user_credits: dict = {"email": "bali@mail.ru", "password": "bali123"}
new_user_credits: dict = {
    "email": user_credits.get("email"),
    "previous_password": user_credits.get("password"),
    "password": "new_pass123",
}

fake_user_credits: dict = {"email": "fake@user.ru", "password": "fake_password"}

role_credits: dict = {"name": "test_role", "access_level": 5}

url_logout: str = address + base_api_url + "/logout"
url_refresh_tokens: str = address + base_api_url + "/refresh-tokens"
url_login: str = address + base_api_url + "/login"
url_registration: str = address + base_api_url + "/registration"
url_change_credits: str = address + base_api_url + "/change-credits"
url_login_history: str = address + base_api_url + "/login-history"

url_update_role: str = address + base_api_url + "/update-role"
url_delete_role: str = address + base_api_url + "/delete-role"
url_get_all_roles: str = address + base_api_url + "/get-all-roles"
