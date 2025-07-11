import strawberry
from typing import List

@strawberry.type
class SegmentType:
    id: int
    origin: str
    destination: str
    distance_km: int = strawberry.field(name="distanceKm") 

@strawberry.input
class SegmentInput:
    origin: str
    destination: str
    distanceKm: int  

@strawberry.type
class RouteType:
    id: int
    name: str
    segments: List[SegmentType]
