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
    def _is_data_resource_role_of(self, data_resource_id: str, role: str) -> bool:
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
    ) -> bool:
        data_resource_claim = self.claims["brighthive-data-resource-claims"].get(
            data_resource_id
        )
        data_perm = f"data:{permission.lower()}"
        assertion = (
            "brighthive-data-resource-claims" in self.claims
            and self.claims["brighthive-data-resource-claims"].get(data_resource_id)
            is not None
            and data_perm
            in self.claims["brighthive-data-resource-claims"]
            .get(data_resource_id)
            .get("permissions", [])
        )
        self.assertions.append(assertion)
        return assertion

    def has_edit_to_data_resource(self, data_resource_id) -> bool:
        assertion = self._has_permission_to_data_resource(data_resource_id, "edit")
        return assertion

    def has_view_to_data_resource(self, data_resource_id) -> bool:
        assertion = self._has_permission_to_data_resource(data_resource_id, "view")
        return assertion

    def has_download_to_data_resource(self, data_resource_id) -> bool:
        assertion = self._has_permission_to_data_resource(data_resource_id, "download")
        return assertion

    def _get_data_resources_with_permission(self, permission: str) -> list:
        data_resources = []
        if "brighthive-data-resource-claims" in self.claims:
            data_resource_claims = self.claims["brighthive-data-resource-claims"]
            data_perm = f"data:{permission.lower()}"
            for data_resource_id, permissions in data_resource_claims.items():
                if data_perm in permissions:
                    data_resources.append(data_resource_id)
        return data_resources

    def get_data_resources_with_view_permission(self) -> list:
        data_resources = self._get_data_resources_with_permission("view")
        return data_resources

    def get_data_resources_with_edit_permission(self) -> list:
        data_resources = self._get_data_resources_with_permission("edit")
        return data_resources

    def get_data_resources_with_download_permission(self) -> list:
        data_resources = self._get_data_resources_with_permission("download")
        return data_resources


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
