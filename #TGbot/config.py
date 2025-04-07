import os
from pathlib import Path

class Config:
    # Telegram
    TOKEN = "6904111754:AAEyyp3bF8DEI7mzwdDRQNOp0ypUsnqZaCU"
    
    # Google Sheets
    SPREADSHEET_ID = "1KG5owm69cHzBosIP-Q2ddF85JQWz_FvQ-NzXV4kZDwM"
    CREDS_PATH = Path("services/creds.json")
    SHEET_NAME = "MENU"
    SHEET_RANGE = "A2:D"
    
    # Markdown
    PARSE_MODE = "MarkdownV2"

    # Cache
    CACHE_TTL = 86400  # 24 часа в секундах
    CACHE_FILE = Path("data/menu_cache.pkl")
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"