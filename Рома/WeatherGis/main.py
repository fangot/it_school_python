from pprint import pprint

from src.cities_api import CitiesAPI
from src.weather_api import WeatherAPI

cities = CitiesAPI()
weather = WeatherAPI()

city = cities.get_city_by_id(524901)

data = weather.get_current(city.latitude, city.longitude)
forecast = weather.get_forecast(city.latitude, city.longitude, days=7)

pprint(city)

pprint(data)

pprint(forecast)