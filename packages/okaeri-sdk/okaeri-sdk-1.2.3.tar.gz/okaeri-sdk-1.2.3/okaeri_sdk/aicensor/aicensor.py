from .model import AiCensorPredictionInfo
from ..client import OkaeriClient, tostring, resolve_token, resolve_timeout, resolve_base_url


@tostring
class AiCensorError(BaseException):
    type: str
    message: str


class AiCensor:
    def __init__(self, token: str, timeout: int = None, base_url: str = None):
        _token = resolve_token("OKAERI_SDK_AICENSOR_TOKEN", token)
        _base_url = base_url if base_url else resolve_base_url("OKAERI_SDK_AICENSOR_BASE_PATH", "https://ai-censor.okaeri.eu")
        _timeout = timeout if timeout else resolve_timeout("OKAERI_SDK_TIMEOUT", 5000)
        self._client = OkaeriClient({'Token': _token}, _base_url, timeout)

    def is_swear(self, phrase) -> bool:
        return self.get_prediction(phrase).general.swear

    def get_prediction(self, phrase) -> AiCensorPredictionInfo:
        return self._client.post("/predict", {'phrase': phrase}, AiCensorPredictionInfo, AiCensorError)
