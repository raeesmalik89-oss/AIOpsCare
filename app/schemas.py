
from pydantic import BaseModel

class PatientData(BaseModel):
    heart_rate: float
    temperature: float
    respiratory_rate: float
