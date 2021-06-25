from bhjwt.exceptions import TokenIsNotJWT, FailedToDecodeJwt
from bhjwt.assertions import AssertJwt
import jwt


class LegacyTokenMixin:
    @staticmethod
    def _verify_not_legacy_access_token(token: str) -> None:
        if not LegacyTokenMixin._token_is_jwt(token):
            raise TokenIsNotJWT(
                http_status_code=400, error_message=f"Bearer token '{token}' is not a JWT.")

    @staticmethod
    def _token_is_jwt(token: str) -> bool:
        return token.find('.') != -1


class PublicKeys:
    @staticmethod
    def get_public_keys():
        return [
            '-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAwejbXvlxa9CBQesoDMUd8Ih7wSn+1UQvkOJL/ueR0d0RZKGLGNSrOaDJDrn7Wexsee0Y4ANQty8l8HDHjsX1GDEt9ZfF7H1QW9QXi8THZOUESagTwZvNpofmB1yEin4ZmKbp80DY0RfZEnRWdvY4VW1KRZCiVgELgGXi4dACOJ8ZvhUfkfaeVcb5hjPbjnbjRhSMsF7IxwHpF0cccEAk+j5Ci8Cho1f5mfkMtYZc2Uugjs4C78wG/O2P2Qr1z3Fv1mapOpkvjJblD/+AJJVHIg/oQHzVpF0VdvDcv5y0g59eNV6pDNsPsrwaaZk10xzOhhVav9RiACEOaojk8nAIc9D4CKHjpyzz78vreCBMffZqf1Khl6LhzGIxYuOVXj/P6NgD7FTFDNTQ8CdETORqdirHkRSYE0yCnO3HvHnX8IpwCW9yWfCM6PBTLLCAxn4GxuJ+/5LkNahZJVlV9aR6BPweU+APTX11XlYig7WIJwUGeqOf6lhqT/w9pWr1utUf8t9wCSY/rNI1mHKAjPl+yYI+VL0VJ018RUQ0GRxcgLOnIdxTSBb2zewpwVV0KyD8BHPueiG6M4vbK1vk6f8Hzlyji3uWLqA+HTBBqGFZX6lAnESSCGJUj6zH0Gf0rTg9mduVtJDHGBONhXtq0JcS3/dqXLVVBfuL1ghs8eOWxm8CAwEAAQ==\n-----END PUBLIC KEY-----'
        ]


class BhJwtValidator(LegacyTokenMixin):
    """Handles the validation process for a BH JWT.

    May raise the following exceptions:
        TokenIsNotJWT
        FailedToDecodeJwt?
    """

    def __init__(self, token: str):
        BhJwtValidator._verify_not_legacy_access_token(token)
        self.validated_claims = self._decode_jwt(token)

    @staticmethod
    def _decode_jwt(encoded_jwt) -> dict:
        for key in PublicKeys.get_public_keys():
            try:
                claims = jwt.decode(
                    encoded_jwt,
                    key,
                    issuer="brighthive-authserver",
                    audience="brighthive-permissions-service",  # TODO: get value from entry point
                    algorithms=["RS256"])

                return claims

            # https://pyjwt.readthedocs.io/en/stable/api.html#exceptions
            except jwt.InvalidTokenError:
                # Public key did not work
                print('public key did not decode jwt')
                pass

            except jwt.ExpiredSignatureError:
                # Signature has expired
                pass  # TODO: raise

            except jwt.InvalidIssuerError:
                # issuer="brighthive-authserver", not present
                pass  # TODO: raise

            except jwt.InvalidAudienceError:
                # JWT was not meant for me!
                pass  # TODO: raise

            except jwt.InvalidIssuedAtError:
                pass  # TODO: raise

        print('JWT Error: Likely the public key did not work.')
        raise FailedToDecodeJwt(
            http_status_code=400,
            error_message="Unable to decode JWT: It is likely the public key did not work."
        )


def create_asserter(token: str) -> AssertJwt:
    validated_claims = BhJwtValidator(token).validated_claims
    asserter = AssertJwt(validated_claims)
    return asserter
