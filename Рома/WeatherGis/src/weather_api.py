import json
import urllib.request
from typing import Optional, Dict, Any


class WeatherAPI:   
    BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    
    def get_current(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        url = (
            f"{self.BASE_URL}"
            f"?latitude={lat}"
            f"&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,"
            f"precipitation,surface_pressure,wind_speed_10m,wind_gusts_10m"
        )
        
        try:
            response = self._fetch(url)
            data = json.loads(response)
            
            if 'current' not in data:
                return
            
            current = data['current']

            pressure_hpa = current.get('surface_pressure')
            pressure_mmhg = None
            if pressure_hpa is not None:
                pressure_mmhg = round(pressure_hpa / 1.333, 1)
            
            wind_speed_kmh = current.get('wind_speed_10m')
            wind_speed_ms = None
            if wind_speed_kmh is not None:
                wind_speed_ms = round(wind_speed_kmh / 3.6, 1)
            
            wind_gusts_kmh = current.get('wind_gusts_10m')
            wind_gusts_ms = None
            if wind_gusts_kmh is not None:
                wind_gusts_ms = round(wind_gusts_kmh / 3.6, 1)
            
            return {
                'temperature': current.get('temperature_2m'),
                'wind_speed': wind_speed_ms,
                'wind_gusts': wind_gusts_ms,
                'precipitation': current.get('precipitation'),
                'pressure': pressure_mmhg,
                'humidity': current.get('relative_humidity_2m'),
            }
        except Exception:
            return
    
    def get_forecast(self, lat: float, lon: float, days: int = 7) -> Optional[Dict[str, Any]]:
        days = min(max(days, 1), 16)
        
        url = (
            f"{self.BASE_URL}"
            f"?latitude={lat}"
            f"&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,"
            f"precipitation,surface_pressure,wind_speed_10m,wind_gusts_10m"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            f"&timezone=auto"
            f"&forecast_days={days}"
        )
        
        try:
            response = self._fetch(url)
            data = json.loads(response)
            
            result = {
                'current': None,
                'daily': [],
            }
            
            if 'current' in data:
                current = data['current']
                
                pressure_hpa = current.get('surface_pressure')
                pressure_mmhg = None
                if pressure_hpa is not None:
                    pressure_mmhg = round(pressure_hpa / 1.333, 1)
                
                wind_speed_kmh = current.get('wind_speed_10m')
                wind_speed_ms = None
                if wind_speed_kmh is not None:
                    wind_speed_ms = round(wind_speed_kmh / 3.6, 1)
                
                wind_gusts_kmh = current.get('wind_gusts_10m')
                wind_gusts_ms = None
                if wind_gusts_kmh is not None:
                    wind_gusts_ms = round(wind_gusts_kmh / 3.6, 1)
                
                result['current'] = {
                    'temperature': current.get('temperature_2m'),
                    'wind_speed': wind_speed_ms,
                    'wind_gusts': wind_gusts_ms,
                    'precipitation': current.get('precipitation'),
                    'pressure': pressure_mmhg,
                    'humidity': current.get('relative_humidity_2m'),
                }
            
            if 'daily' in data:
                daily = data['daily']
                dates = daily.get('time', [])
                temps_max = daily.get('temperature_2m_max', [])
                temps_min = daily.get('temperature_2m_min', [])
                precip = daily.get('precipitation_sum', [])
                
                for i in range(len(dates)):
                    day_data = {
                        'date': dates[i] if i < len(dates) else None,
                        'temp_max': temps_max[i] if i < len(temps_max) else None,
                        'temp_min': temps_min[i] if i < len(temps_min) else None,
                        'precipitation': precip[i] if i < len(precip) else None,
                    }
                    result['daily'].append(day_data)
            
            return result
        except Exception:
            return
    
    def _fetch(self, url: str) -> str:
        with urllib.request.urlopen(url, timeout=10) as response:
            return response.read().decode('utf-8')
