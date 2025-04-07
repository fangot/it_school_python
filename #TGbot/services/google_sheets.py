from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Optional, Dict, Any
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config import Config
from services.cache import MenuCache

class GoogleSheetsService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.creds = self._get_credentials()
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.cache = MenuCache()
        self.last_etag = None

    def _get_credentials(self):
        """Получение учетных данных Google"""
        try:
            return service_account.Credentials.from_service_account_file(
                Config.CREDS_PATH,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
        except Exception as e:
            self.logger.error(f"Ошибка загрузки учетных данных: {e}")
            raise

    def get_data(self, range_name: str) -> Optional[List[List[str]]]:
        """Основной метод получения данных"""
        try:
            # Пробуем получить из кэша
            if cached := self._try_get_cached(range_name):
                return cached
            
            # Если нет в кэше, загружаем свежие данные
            if fresh_data := self._fetch_raw_data(range_name):
                return fresh_data.get(range_name)
                
            return None
        except Exception as e:
            self.logger.error(f"Ошибка получения данных: {e}")
            return None

    def _try_get_cached(self, range_name: str) -> Optional[List[List[str]]]:
        """Попытка получить данные из кэша"""
        if cached := self.cache.get():
            if cached_range := cached.get(range_name):
                self.logger.debug(f"Данные получены из кэша для диапазона {range_name}")
                return cached_range
        return None

    def _fetch_raw_data(self, range_name: str) -> Optional[Dict[str, List[List[str]]]]:
        """Получение свежих данных из таблицы"""
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=Config.SPREADSHEET_ID,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            normalized = self._normalize_data(values)
            
            cache_data = {range_name: normalized}
            self.cache.update(cache_data)
            
            self.logger.info(f"Данные успешно обновлены для диапазона {range_name}")
            return cache_data
        except HttpError as error:
            self.logger.error(f"Ошибка Google Sheets API: {error}")
            # Проверяем конкретный тип ошибки
            if error.resp.status == 400:
                self.logger.error("Проверьте правильность указания диапазона и прав доступа")
            return None
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка: {e}")
            return None

    def _normalize_data(self, data: List[List[str]]) -> List[List[str]]:
        """Нормализация данных (выравнивание строк)"""
        if not data:
            return []
            
        max_cols = max(len(row) for row in data)
        return [row + [''] * (max_cols - len(row)) for row in data]

    def check_connection(self) -> bool:
        """Проверка соединения с Google Sheets"""
        try:
            self.service.spreadsheets().values().get(
                spreadsheetId=Config.SPREADSHEET_ID,
                range="A1",
                majorDimension="ROWS"
            ).execute()
            return True
        except Exception as e:
            self.logger.error(f"Ошибка соединения: {e}")
            return False