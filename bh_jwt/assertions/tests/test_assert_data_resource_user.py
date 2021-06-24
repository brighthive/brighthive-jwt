from bh_jwt.assertions.main import AssertJwt
from bh_jwt.exceptions import AuthorizationError
import pytest

# Super Admin claims


def test_pass_if_dr_role_claim_is_correct():
    asserter = AssertJwt({
        "brighthive-data-resource-claims": {
            "test-dr": {
                "role": "user"
            }
        }})
    asserter.is_data_resource_user_of('test-dr')
    asserter.fail_if_none()


def test_fail_if_dr_role_not_present():
    asserter = AssertJwt({"brighthive-data-resource-claims": {}})
    asserter.is_data_resource_user_of('test-dr')

    with pytest.raises(AuthorizationError):
        asserter.fail_if_none()


def test_fail_if_dr_role_is_incorrect():
    asserter = AssertJwt({
        "brighthive-data-resource-claims": {
            "test-dr": {
                "role": "admin"
            }
        }})
    asserter.is_data_resource_user_of('test-dr')

    with pytest.raises(AuthorizationError):
        asserter.fail_if_none()
