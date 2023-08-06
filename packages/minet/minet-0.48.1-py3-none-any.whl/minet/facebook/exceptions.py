# =============================================================================
# Minet Facebook Exceptions
# =============================================================================
#
from minet.exceptions import MinetError


class FacebookError(MinetError):
    pass


class FacebookInvalidCookieError(FacebookError):
    pass
