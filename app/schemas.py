
from pydantic import BaseModel

class PatientData(BaseModel):
    HR: float
    O2Sat: float
    Temp: float
    SBP: float
    MAP: float
    Resp: float
    Age: float
    ICULOS: float
