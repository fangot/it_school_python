import shutil
import sqlite3
import tempfile
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

from .db_manager import DBManager
from .city import City
from .country import Country


class CitiesAPI:
    DATA_SOURCES: Dict[str, str] = {
        "cities15000": "http://download.geonames.org/export/dump/cities15000.zip",
        "cities5000": "http://download.geonames.org/export/dump/cities5000.zip",
        "cities1000": "http://download.geonames.org/export/dump/cities1000.zip",
    }
    COUNTRIES_URL: str = "http://download.geonames.org/export/dump/countryInfo.txt"
    DEFAULT_DB_PATH: Path = Path(__file__).parent / "db" / "cities_database.sqlite"
    
    def __init__(self, db_path: Optional[str] = None, data_source: str = "cities15000") -> None:
        if db_path:
            self.db_path: Path = Path(db_path)
        else:
            self.db_path: Path = self.DEFAULT_DB_PATH
        #self.db_path: Path = Path(db_path) if db_path else self.DEFAULT_DB_PATH
        self._countries: Dict[str, str] = {}
        self.db: DBManager = None
        
        if self.db_path.exists():
            self.db = DBManager(str(self.db_path))
        else:
            self._create_database(data_source)
    
    def _create_database(self, data_source: str) -> None:
        temp_dir = Path(tempfile.mkdtemp(prefix="geonames_"))
        try:
            self.db = DBManager(str(self.db_path))
            self._create_schema()
            
            file = self._download(self.COUNTRIES_URL, temp_dir)
            self._import_countries(file)
            
            url = self.DATA_SOURCES[data_source]
            file = self._download(url, temp_dir)
            file = self._unzip(file, temp_dir)
            self._import_cities(file)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _create_schema(self) -> None:
        self.db.create_table('countries', {'code': 'TEXT', 'name': 'TEXT'}, pk='code')
        self.db.create_table('cities', {
            'id': 'INTEGER',
            'geonameid': 'INTEGER UNIQUE',
            'name': 'TEXT NOT NULL',
            'asciiname': 'TEXT',
            'latitude': 'REAL NOT NULL',
            'longitude': 'REAL NOT NULL',
            'country_code': 'TEXT',
            'country_name': 'TEXT',
            'population': 'INTEGER',
            'timezone': 'TEXT',
            'feature_code': 'TEXT',
            'admin1_code': 'TEXT',
            'admin2_code': 'TEXT',
            'elevation': 'INTEGER',
            'modification_date': 'TEXT'
        }, pk='id')
        self.db.create_index('cities', ['name'])
        self.db.create_index('cities', ['country_code'])
    
    def _download(self, url: str, dest: Path) -> Path:
        path = dest / url.split('/')[-1]
        urllib.request.urlretrieve(url, path)
        return path
    
    def _unzip(self, zip_path: Path, dest: Path) -> Path:
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(dest)
        for f in dest.iterdir():
            if f.suffix == '.txt':
                return f
        raise FileNotFoundError("Нет .txt в архиве")
    
    def _import_countries(self, filepath: Path) -> None:
        with open(filepath, encoding='utf-8') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                parts = line.strip().split('\t')
                if len(parts) >= 5:
                    code, name = parts[0], parts[4]
                    self._countries[code] = name
                    self.db.insert('countries', {'code': code, 'name': name}, replace=True)
    
    def _import_cities(self, filepath: Path) -> None:
        batch: List[Dict[str, Any]] = []
        with open(filepath, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) < 15:
                    continue
                try:
                    cc = parts[8] if len(parts) > 8 else None
                    batch.append({
                        'geonameid': int(parts[0]),
                        'name': parts[1],
                        'asciiname': parts[2] if len(parts) > 2 else parts[1],
                        'latitude': float(parts[4]),
                        'longitude': float(parts[5]),
                        'country_code': cc,
                        'country_name': self._countries.get(cc),
                        'population': int(parts[14]) if parts[14] else 0,
                        'timezone': parts[17] if len(parts) > 17 else None,
                        'feature_code': parts[7] if len(parts) > 7 else None,
                        'admin1_code': parts[10] if len(parts) > 10 else None,
                        'admin2_code': parts[11] if len(parts) > 11 else None,
                        'elevation': int(parts[15]) if len(parts) > 15 and parts[15] else None,
                        'modification_date': parts[18] if len(parts) > 18 else None,
                    })
                    if len(batch) >= 5000:
                        self.db.insert_many('cities', batch, replace=True)
                        batch = []
                except (ValueError, IndexError):
                    continue
        if batch:
            self.db.insert_many('cities', batch, replace=True)
    
    def get_city_by_id(self, geonameid: int) -> Optional[City]:
        sql = "SELECT * FROM cities WHERE geonameid = ?"
        row = self.db.fetch_one(sql, (geonameid,))
        if row is None:
            return
        
        return self._to_city(row)
    
    def get_city_by_name(self, name: str, country_code: Optional[str] = None) -> Optional[City]:
        if country_code:
            sql = "SELECT * FROM cities WHERE name = ? AND country_code = ? LIMIT 1"
            row = self.db.fetch_one(sql, (name, country_code))
        else:
            sql = "SELECT * FROM cities WHERE name = ? LIMIT 1"
            row = self.db.fetch_one(sql, (name,))
 
        if row is None:
            return
        
        return self._to_city(row)
    
    def search_cities(self, query: str, limit: int = 20) -> List[City]:
        sql = "SELECT * FROM cities WHERE name LIKE ? ORDER BY population DESC LIMIT ?"
        rows = self.db.fetch_all(sql, (f"%{query}%", limit))
        result = []
        for r in rows:
            result.append(self._to_city(r))
        
        return result
    
    def find_by_country(
        self,
        country_code: str,
        min_population: int = 0,
        limit: Optional[int] = None
    ) -> List[City]:
        sql = "SELECT * FROM cities WHERE country_code = ? AND population >= ? ORDER BY population DESC"
        if limit:
            sql += f" LIMIT {limit}"
        
        rows = self.db.fetch_all(sql, (country_code, min_population))
        result = []
        for r in rows:
            result.append(self._to_city(r))
        
        return result
    
    def get_all_ids(self, country_code: Optional[str] = None, min_population: int = 0) -> List[int]:
        conds: List[str] = ["population >= ?"]
        params: List[Any] = [min_population]
        
        if country_code:
            conds.append("country_code = ?")
            params.append(country_code)

        sql = f"SELECT geonameid FROM cities WHERE {' AND '.join(conds)}"
        rows = self.db.fetch_all(sql, tuple(params))
        result = []
        for r in rows:
            result.append(r[0])
        
        return result
    
    def get_all_cities(
        self,
        country_code: Optional[str] = None,
        min_population: int = 0,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[City]:
        conds: List[str] = ["population >= ?"]
        params: List[Any] = [min_population]
        
        if country_code:
            conds.append("country_code = ?")
            params.append(country_code)
        
        sql = f"SELECT * FROM cities WHERE {' AND '.join(conds)} ORDER BY population DESC"
        if limit:
            sql += f" LIMIT {limit} OFFSET {offset}"
        
        rows = self.db.fetch_all(sql, tuple(params))
        result = []
        for r in rows:
            result.append(self._to_city(r))
        
        return result
    
    def get_cities_list(
        self,
        fields: Optional[List[str]] = None,
        country_code: Optional[str] = None,
        min_population: int = 0,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        valid = [
            'geonameid',
            'name',
            'latitude',
            'longitude',
            'country_code', 
            'country_name',
            'population',
            'timezone'
        ]
        
        if fields is None:
            fields = ['geonameid', 'name', 'country_name', 'latitude', 'longitude', 'population']
        
        filtered_fields = []
        for f in fields:
            if f in valid:
                filtered_fields.append(f)
        fields = ', '.join(filtered_fields)
        
        conds: List[str] = ["population >= ?"]
        params: List[Any] = [min_population]
        
        if country_code:
            conds.append("country_code = ?")
            params.append(country_code)
        
        sql = f"SELECT {fields} FROM cities WHERE {' AND '.join(conds)} ORDER BY population DESC"
        if limit:
            sql += f" LIMIT {limit}"
        
        rows = self.db.fetch_all(sql, tuple(params))
        result = []
        for r in rows:
            result.append(dict(r))
        
        return result
    
    def count_all(self, country_code: Optional[str] = None, min_population: int = 0) -> int:
        conds: List[str] = ["population >= ?"]
        params: List[Any] = [min_population]
        
        if country_code:
            conds.append("country_code = ?")
            params.append(country_code)
        
        return self.db.count('cities', ' AND '.join(conds), tuple(params))
    
    def _to_city(self, row: sqlite3.Row) -> City:
        return City(
            geonameid=row['geonameid'],
            name=row['name'],
            asciiname=row['asciiname'],
            latitude=row['latitude'],
            longitude=row['longitude'],
            country_code=row['country_code'],
            country_name=row['country_name'],
            population=row['population'],
            timezone=row['timezone'],
            feature_code=row['feature_code'],
            admin1_code=row['admin1_code'],
            admin2_code=row['admin2_code'],
            elevation=row['elevation'],
            modification_date=row['modification_date']
        )
    
    def close(self) -> None:
        self.db.close()
