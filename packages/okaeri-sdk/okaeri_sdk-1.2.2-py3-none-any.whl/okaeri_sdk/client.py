import json
import requests
import marshmallow_dataclass
import os

from typing import TypeVar, Type, Dict

T = TypeVar('T')
E = TypeVar('E')


def tostring(obj):
    def __str__(self):
        return f"({', '.join('%s=%s' % v for v in vars(self).items())})"

    obj.__str__ = __str__
    return obj


@tostring
class OkaeriError(BaseException):
    message: str


def resolve_token(env_name: str, value: str):
    if value:
        return value
    if env_name in os.environ:
        return os.environ[env_name]
    raise OkaeriError("token cannot be null or empty")


def resolve_timeout(env_name: str, default_value: int):
    return int(os.environ[env_name]) if env_name in os.environ else default_value


def resolve_base_url(env_name: str, default_value: str):
    return os.environ[env_name] if env_name in os.environ else default_value


class OkaeriClient:
    def __init__(self, headers: Dict[str, str], base_url: str, timeout: int = 5000):
        self._headers = headers
        self._base_url = base_url
        self._timeout = timeout

    @staticmethod
    def _convert(data: str, clazz: Type[T]) -> T:
        schema = marshmallow_dataclass.class_schema(clazz)()
        return schema.load(data)

    def _request(self, url: str, clazz: Type[T], err: Type[E], method: str = "GET", data: object = None) -> T:
        try:
            if method == "GET":
                request = requests.get(url=f"{self._base_url}{url}", headers=self._headers)
            elif method == "POST":
                request = requests.post(url=f"{self._base_url}{url}", json=data, headers=self._headers)
            else:
                raise OkaeriError(f"Unknown method: {method}")
        except requests.exceptions.RequestException as exception:
            raise OkaeriError(str(exception))
        try:
            parsed = request.json()
        except json.decoder.JSONDecodeError as error:
            raise OkaeriError(f"Server returned invalid json: {str(error)}")
        if request.status_code != 200:
            raise self._convert(parsed, err)
        return self._convert(parsed, clazz)

    def get(self, url: str, clazz: Type[T], err: Type[E]) -> T:
        return self._request(url, clazz, err, "GET")

    def post(self, url: str, data: object, clazz: Type[T], err: Type[E]) -> T:
        return self._request(url, clazz, err, "POST", data)
