"""OAuth 2.0 Providers

This module contains implementation-specific methods for all OAuth 2.0
providers supported by the library.

Note:
    To add a new provider, ensure that the provider extends the OAuth2Provider
    base class.

"""

from bhjwt.providers.provider_error import OAuth2ProviderError
from bhjwt.providers.provider import OAuth2Provider
from bhjwt.providers.brighthive_provider import BrightHiveProvider
from bhjwt.providers.provider_factory import OAuth2ProviderFactory
