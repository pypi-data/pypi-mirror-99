from dataclasses import dataclass
from okaeri_sdk.client import tostring


@tostring
@dataclass
class NoProxyAddressInfoGeneral:
    ip: str
    asn: int
    provider: str
    country: str


@tostring
@dataclass
class NoProxyAddressInfoRisks:
    total: int
    proxy: bool
    country: bool
    asn: bool
    provider: bool
    abuser: bool


@tostring
@dataclass
class NoProxyAddressInfoScore:
    noproxy: int
    abuseipdb: int


@tostring
@dataclass
class NoProxyAddressInfoSuggestions:
    verify: bool
    block: bool


@tostring
@dataclass
class NoProxyAddressInfo:
    general: NoProxyAddressInfoGeneral
    risks: NoProxyAddressInfoRisks
    score: NoProxyAddressInfoScore
    suggestions: NoProxyAddressInfoSuggestions
