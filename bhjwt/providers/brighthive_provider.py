"""BrightHive OAuth 2.0 Provider.

Implementation of a BrightHive OAuth 2.0 Provier.

"""

import requests
import json
from bhjwt.providers import OAuth2Provider, OAuth2ProviderError
from bhjwt.main import create_asserter


class BrightHiveProvider(OAuth2Provider):
    """BrightHive OAuth 2.0 Provider."""

    def __init__(self):
        super().__init__()

    def validate_token(self, token=None, scopes=[]):
        if not token:
            token = self.get_token()

        try:
            # headers = {'content-type': 'application/json'}
            # validate_ep = f'{self.base_url}/oauth/validate'
            # payload = {'token': token}
            # query = requests.post(
            #     validate_ep, data=json.dumps(payload), headers=headers)
            # resp = query.json()
            # if resp['messages']['valid']:
            #     return True
            try:
                asserter = create_asserter(token)
            except Exception:
                raise OAuth2ProviderError("Access Denied")
            return asserter.claims
        except Exception:
            raise OAuth2ProviderError("Access Denied")
