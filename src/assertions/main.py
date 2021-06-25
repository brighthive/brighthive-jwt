from src.exceptions import AuthorizationError


class AdminAssertions:
    def is_super_admin(self):
        assertion = "brighthive-super-admin" in self.claims and self.claims["brighthive-super-admin"] == True
        self.assertions.append(assertion)


class DataResourceRoleAssertions:
    def _is_data_resource_role_of(self, data_resource_id: str, role: str) -> None:
        assertion = "brighthive-data-resource-claims" in self.claims and self.claims[
            "brighthive-data-resource-claims"].get(data_resource_id) is not None and \
            self.claims["brighthive-data-resource-claims"][data_resource_id].get("role",
                                                                                 "").lower() == role.lower()
        self.assertions.append(assertion)

    def is_data_resource_admin_of(self, data_resource_id):
        self._is_data_resource_role_of(data_resource_id, "admin")

    def is_data_resource_user_of(self, data_resource_id):
        self._is_data_resource_role_of(data_resource_id, "user")


class AssertJwt(AdminAssertions, DataResourceRoleAssertions):
    def __init__(self, claims):
        self._claims = claims
        self.assertions = []

    @property
    def claims(self):
        return self._claims

    def fail_if_none(self):
        if not any(self.assertions):
            raise AuthorizationError(
                http_status_code=403, error_message="JWT does not have the necessary claims to perform this action.")

