from typing import Optional
from pydantic import BaseModel


### Used to construct a post request
class SensorPayload(BaseModel):
    timestamp: Optional[int]
    key:str
    unit:str
    value: float
    lat:Optional[float]
    lon:Optional[float]

