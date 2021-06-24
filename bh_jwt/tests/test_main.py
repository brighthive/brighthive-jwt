from bh_jwt import create_asserter
from bh_jwt.assertions import AssertJwt
from bh_jwt.main import BhJwtValidator, LegacyTokenMixin
from bh_jwt.exceptions import FailedToDecodeJwt, TokenIsNotJWT
import pytest


def test_token_is_jwt():
    assert LegacyTokenMixin._token_is_jwt('invalid') is False
    assert LegacyTokenMixin._token_is_jwt('token.token.token') is True


def test_verify_not_legacy_access_token():
    with pytest.raises(TokenIsNotJWT):
        LegacyTokenMixin._verify_not_legacy_access_token('invalid')

    LegacyTokenMixin._verify_not_legacy_access_token('token.token.token')


def test_fails_when_invalid_jwt_provided():
    with pytest.raises(TokenIsNotJWT):
        BhJwtValidator('invalid')


def test_error_with_invalid_jwt():
    with pytest.raises(TokenIsNotJWT):
        create_asserter('invalid')

# Main


# def test_successfully_creates_asserter():
#     asserter = create_asserter('insert_real_jwt')
#     assert isinstance(asserter, AssertJwt)


def test_fails_with_unsigned_jwt():
    with pytest.raises(FailedToDecodeJwt):
        create_asserter('invalid.invalid.invalid')

# Assert known claims fail as expected


def test_fails_with_expired_jwt():
    pass


def test_fails_when_i_am_not_in_audience():
    pass


def test_fails_when_issuer_is_not_bh_authserver():
    pass
