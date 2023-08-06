from typing import Any

from us_libraries.client.base_client import BaseClient

service_name = "usf-auth-service"


class AuthClient(BaseClient):

    def __init__(self) -> None:
        super().__init__(service_name)

    def login(self, username: str, password: str) -> Any:
        return self.post('login', username=username, password=password)

    def has_permission(self, login_token: str, permission_id: int, permission_name: str) -> Any:
        return self.get(f'permission/has_permission?login_token={login_token}'
                        f'&permission_id={permission_id}&permission_name={permission_name}')

    def logout(self, login_token: str) -> Any:
        return self.get('logout/%s' % login_token)

    def generate_otp(self, auth_user_id: int) -> Any:
        return self.get('generate_otp/%s' % auth_user_id)
