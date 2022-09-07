
from dataclasses import dataclass
from typing import List

def MakeBlankMeasurementData():
    return MeasurementData([],[],[],[],[],[])

@dataclass
class MeasurementData:
    sample: List[int]
    step: List[float]
    load: List[float]
    phase: List[int]
    maxLoad: List[int]
    VASScores: List[int]
    filename: str = ""

