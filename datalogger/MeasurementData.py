
from dataclasses import dataclass
from typing import List



@dataclass
class MeasurementData:
    sample: List[int]
    step: List[float]
    load: List[float]
    initialApproachStart: int = -1
    preloadHoldStart: int = -1
    mainApproachStart: int = -1
    mainHoldStart:int = -1
    retractStart: int = -1
    filename: str = ""

