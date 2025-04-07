import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import pickle
import os
import logging
from pathlib import Path

class MenuCache:
    def __init__(self, cache_ttl: int = 86400):  # 24 часа в секундах
        self.logger = logging.getLogger(__name__)
        self.cache_ttl = timedelta(seconds=cache_ttl)
        self.last_updated: Optional[datetime] = None
        self.cache_data: Optional[Dict[str, Any]] = None
        self.cache_file = Path("data/menu_cache.pkl")
        self.lock = threading.Lock()
        
        # Создаем папку для кэша, если её нет
        os.makedirs(self.cache_file.parent, exist_ok=True)
        self._load_cache()

    def _load_cache(self):
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'rb') as f:
                    data = pickle.load(f)
                    if isinstance(data, dict):  # Проверка структуры
                        self.cache_data = data.get('cache_data')
                        self.last_updated = data.get('last_updated')
                        self.logger.info("Кэш успешно загружен из файла")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки кэша: {e}")
            self.cache_data = None
            self.last_updated = None

    def _save_cache(self):
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump({
                    'cache_data': self.cache_data,
                    'last_updated': self.last_updated
                }, f)
            self.logger.info("Кэш успешно сохранен")
        except Exception as e:
            self.logger.error(f"Ошибка сохранения кэша: {e}")

    def is_valid(self) -> bool:
        """Проверяем актуальность кэша"""
        if not self.last_updated or not self.cache_data:
            return False
        return (datetime.now() - self.last_updated) < self.cache_ttl

    def get(self) -> Optional[Dict[str, Any]]:
        """Получаем данные из кэша"""
        with self.lock:
            return self.cache_data if self.is_valid() else None

    def update(self, data: Dict[str, Any]):
        """Обновляем кэш"""
        with self.lock:
            self.cache_data = data
            self.last_updated = datetime.now()
            self._save_cache()

    def start_auto_refresh(self, refresh_callback, interval: int = 86400):
        """Запускаем автоматическое обновление"""
        def refresh_worker():
            while True:
                time.sleep(interval)
                try:
                    new_data = refresh_callback()
                    if new_data:
                        self.update(new_data)
                except Exception as e:
                    print(f"Cache refresh error: {e}")

        thread = threading.Thread(target=refresh_worker, daemon=True)
        thread.start()