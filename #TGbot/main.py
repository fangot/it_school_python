from bot.core import TelegramBot
import logging

def check_dependencies():
    try:
        import google
        import telebot
        # ... другие важные импорты ...
    except ImportError as e:
        print(f"Ошибка: Не установлены зависимости - {e}")
        print("Установите их командой: pip install -r requirements.txt")
        exit(1)

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )

if __name__ == "__main__":
    check_dependencies()
    configure_logging()
    
    logger = logging.getLogger(__name__)
    logger.info("Запуск бота...")
    
    try:
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}", exc_info=True)