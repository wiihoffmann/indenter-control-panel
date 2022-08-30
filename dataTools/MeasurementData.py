
from dataclasses import dataclass
from typing import List



@dataclass
class MeasurementData:
    sample: List[int]
    step: List[float]
    load: List[float]
    phase: List[int]
    measurementType: bytes
    filename: str = ""

