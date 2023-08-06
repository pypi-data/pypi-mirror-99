from .model import NoProxyAddressInfo
from ..client import OkaeriClient, tostring, resolve_base_url, resolve_timeout, resolve_token


@tostring
class NoProxyError(BaseException):
    type: str
    message: str


class NoProxy:
    def __init__(self, token: str, timeout: int = None, base_url: str = None):
        _token = resolve_token("OKAERI_SDK_NOPROXY_TOKEN", token)
        _base_url = base_url if base_url else resolve_base_url("OKAERI_SDK_NOPROXY_BASE_PATH", "https://noproxy-api.okaeri.eu")
        _timeout = timeout if timeout else resolve_timeout("OKAERI_SDK_TIMEOUT", 5000)
        self._client = OkaeriClient({'Authorization': f"Bearer {_token}"}, _base_url, timeout)

    def get_info(self, address) -> NoProxyAddressInfo:
        return self._client.get(f"/v1/{address}", NoProxyAddressInfo, NoProxyError)
