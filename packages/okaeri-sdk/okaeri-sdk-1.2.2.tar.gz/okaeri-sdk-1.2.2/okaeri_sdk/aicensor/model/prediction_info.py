from dataclasses import dataclass, field
from typing import List
from okaeri_sdk.client import tostring


@tostring
@dataclass
class AiCensorPredictionInfoGeneral:
    swear: bool
    breakdown: str
    domains: bool


@tostring
@dataclass
class AiCensorPredictionInfoDetails:
    basic_contains_hit: bool
    exact_match_hit: bool
    ai_label: str
    ai_probability: float
    domains_list: List[str] = field(default_factory=list)


@tostring
@dataclass
class AiCensorPredictionInfoElapsed:
    all: float
    processing: float


@tostring
@dataclass
class AiCensorPredictionInfo:
    general: AiCensorPredictionInfoGeneral
    details: AiCensorPredictionInfoDetails
    elapsed: AiCensorPredictionInfoElapsed
