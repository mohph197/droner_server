from pydantic import BaseModel


class Point(BaseModel):
    lon: float
    lat: float
