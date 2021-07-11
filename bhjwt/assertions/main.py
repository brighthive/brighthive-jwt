from bhjwt.exceptions import AuthorizationError


class AdminAssertions:
    def is_super_admin(self):
        assertion = (
            "brighthive-super-admin" in self.claims
            and self.claims["brighthive-super-admin"] == True
        )
        self.assertions.append(assertion)
        return assertion


class DataResourceAssertions:
    def _is_data_resource_role_of(self, data_resource_id: str, role: str) -> None:
        assertion = (
            "brighthive-data-resource-claims" in self.claims
            and self.claims["brighthive-data-resource-claims"].get(data_resource_id)
            is not None
            and self.claims["brighthive-data-resource-claims"][data_resource_id]
            .get("role", "")
            .lower()
            == role.lower()
        )
        self.assertions.append(assertion)
        return assertion

    def is_data_resource_admin_of(self, data_resource_id):
        assertion = self._is_data_resource_role_of(data_resource_id, "admin")
        return assertion

    def is_data_resource_user_of(self, data_resource_id):
        assertion = self._is_data_resource_role_of(data_resource_id, "user")
        return assertion

    def _has_permission_to_data_resource(
        self, data_resource_id: str, permission: str
    ) -> None:
        data_resource_claim = self.claims["brighthive-data-resource-claims"].get(
            data_resource_id
        )
        data_perm = f"data:{permission.lower()}"
        assertion = (
            "brighthive-data-resource-claims" in self.claims
            and data_resource_claim is not None
            and data_perm in data_resource_claim.get("permissions", [])
        )
        self.assertions.append(assertion)
        return assertion

    def has_edit_to_data_resource(self, data_resource_id):
        assertion = self._has_permission_to_data_resource(data_resource_id, "edit")
        return assertion

    def has_view_to_data_resource(self, data_resource_id):
        assertion = self._has_permission_to_data_resource(data_resource_id, "view")
        return assertion

    def has_download_to_data_resource(self, data_resource_id):
        assertion = self._has_permission_to_data_resource(data_resource_id, "download")
        return assertion


class AssertJwt(AdminAssertions, DataResourceAssertions):
    def __init__(self, claims):
        self._claims = claims
        self.assertions = []

    @property
    def claims(self):
        return self._claims

    def fail_if_none(self):
        if not any(self.assertions):
            raise AuthorizationError(
                http_status_code=403,
                error_message="JWT does not have the necessary claims to perform this action.",
            )
