from models.api import SensorPayload
#from models.geojson import PointGeometry, GeoJSONFeature, PointGeometry
import requests
from pydantic import ValidationError
import pandas as pd


class IOTInterface():

	def __valdiate_request__(self, r:requests.Response) -> bool:
		return r.status_code == 200

	def __host_available__(self):
		r = requests.get(f"{self.host}/health", verify = False)
		return self.__valdiate_request__(r)

	def __init__(self, host  = ""):
		self.host = host
		if not self.__host_available__():
			raise Exception(f"Unable to establish contact with the following host: {self.host}")

	def post_sensor(self, key, unit, value, lat, lon , timestamp):
		try:
			model = SensorPayload(key=key,
								  unit = unit,
								  value = value,
								  lat = lat,
								  lon = lon,
								  timestamp = timestamp
								  )
		except ValidationError as e:
			raise  e

		if not self.__host_available__():
			raise Exception(f"Unable to establish contact with the following host: {self.host}")

		r = requests.post(f'{self.host}/api/v0p1/sensor', json= dict(model), verify = False)


		if not self.__valdiate_request__(r):
			raise Exception(f"Unable to post sensor payload. Error: {r.status_code}")

	def list_sensors(self):
		if not self.__host_available__():
			raise Exception(f"Unable to establish contact with the following host: {self.host}")

		r = requests.get(f'{self.host}/api/v0p1/list_sensors', verify = False)

		return pd.DataFrame(r.json())



	def get_sensor(self, key = None,
				   min_time = None,
				   max_time = None,
				   min_lat = None,
				   max_lat = None,
				   min_lon = None,
				   max_lon = None):

		data = {}

		if min_time is not None:
			data.update(dict(min_time = min_time))
		if max_time is not None:
			data.update(dict(max_time = max_time))

		if min_lat is not None:
			data.update(dict(min_lat = min_lat))
		if max_time is not None:
			data.update(dict(max_lat = max_lat))

		if min_lon is not None:
			data.update(dict(min_lon = min_lon))
		if max_lon is not None:
			data.update(dict(max_lon = max_lon))

		if not self.__host_available__():
			raise Exception(f"Unable to establish contact with the following host: {self.host}")

		print(data)
		r = requests.get(f"{self.host}/api/v0p1/sensor_by_id/{key}", params = data, verify = False)
		return pd.DataFrame(r.json())



if __name__ == "__main__":
	import time

	def get_username():
		import os
		import pwd
		return pwd.getpwuid(os.getuid())[0].lower()

	def get_pc_location():
		r = requests.get("https://api.ipgeolocationapi.com/geolocate")
		lat = r.json()['geo']['latitude_dec']
		lon = r.json()['geo']['latitude_dec']
		return lat, lon

	node = IOTInterface(host= "https://api.is-conic.com")


	lat,lon = get_pc_location()
	this_computers_key = f"test_mainpy_on_{get_username()}_computer"
	print(f"KEY::::{this_computers_key}")
	print(node.list_sensors())

	node.post_sensor(key = this_computers_key, lat = lat, lon = lon, timestamp= time.time(), unit = "is_posted", value= 1)

	# print(node.get_sensor(key = this_computers_key , max_time= 0 )[["timestamp","unit","value"]])

	print(node.get_sensor(key = this_computers_key , min_time= 1616097811 )[["timestamp","unit","value"]])

