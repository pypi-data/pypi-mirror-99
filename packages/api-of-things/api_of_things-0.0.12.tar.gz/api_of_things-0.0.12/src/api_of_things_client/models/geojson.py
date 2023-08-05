from typing import Dict, List
from pydantic import BaseModel
from abc import ABC


class Geometry(ABC):
	pass

class PointGeometry(BaseModel, Geometry):
	type: str = "Point"
	coordinates: List


class GeoJSONFeature(BaseModel):
	type: str = "Feature"
	properties: Dict = {}
	geometry: Geometry


class GeoJSONFeatureCollection(BaseModel):
	type: str = "FeatureCollection"
	features: List[GeoJSONFeature]