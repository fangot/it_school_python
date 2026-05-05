from pprint import pprint
from random import choice

from src2.db_manager import DBManager
from pathlib import Path

DEFAULT_DB_PATH: Path = Path(__file__).parent / "db" / "cities_database.sqlite"

db = DBManager(str(DEFAULT_DB_PATH))
res = db.select("cities")
pprint(res)

#from src2.cities_api import CitiesAPI
#from src.weather_api import WeatherAPI

#cities = CitiesAPI()
#weather = WeatherAPI()

#all_city = cities.get_all_ids()

#city = cities.get_city_by_id(choice(all_city))

#data = weather.get_current(city.latitude, city.longitude)
#forecast = weather.get_forecast(city.latitude, city.longitude, days=7)

#pprint([city.country_name, city.name])

#pprint(data)

#pprint(forecast)