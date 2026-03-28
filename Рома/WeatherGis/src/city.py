from typing import Dict, Any, Optional


class City:    
    def __init__(
        self,
        geonameid: int,
        name: str,
        latitude: float,
        longitude: float,
        country_code: str,
        country_name: Optional[str] = None,
        population: int = 0,
        timezone: Optional[str] = None,
        feature_code: Optional[str] = None,
        admin1_code: Optional[str] = None,
        admin2_code: Optional[str] = None,
        elevation: Optional[int] = None,
        modification_date: Optional[str] = None,
        asciiname: Optional[str] = None
    ) -> None:
        self.geonameid = geonameid
        self.name = name
        self.asciiname = asciiname if asciiname is not None else name
        self.latitude = latitude
        self.longitude = longitude
        self.country_code = country_code
        self.country_name = country_name
        self.population = population
        self.timezone = timezone
        self.feature_code = feature_code
        self.admin1_code = admin1_code
        self.admin2_code = admin2_code
        self.elevation = elevation
        self.modification_date = modification_date
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'geonameid': self.geonameid,
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'country_code': self.country_code,
            'country_name': self.country_name,
            'population': self.population,
            'timezone': self.timezone,
        }
