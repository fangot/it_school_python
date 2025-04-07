import telebot
from telebot.types import Message, ReplyKeyboardMarkup
import logging
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path
import sys

# Добавляем корень проекта в PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from config import Config
from services.google_sheets import GoogleSheetsService
from bot.menus import MenuItem, MenuManager
from bot.keyboards import KeyboardGenerator

class TelegramBot:
    def __init__(self):
        # Инициализация логгера
        self._init_logger()
        
        # Основные компоненты
        self.bot = telebot.TeleBot(Config.TOKEN)
        self.sheets = GoogleSheetsService()
        self.keyboard_generator = KeyboardGenerator()
        self.menu_manager: Optional[MenuManager] = None
        self.user_states: Dict[int, MenuItem] = {}  # chat_id: current_menu_item
        
        # Загрузка меню
        self._load_menu()
        
        # Регистрация обработчиков
        self._register_handlers()
        
        self.logger.info("Бот успешно инициализирован")

    def _init_logger(self):
        """Инициализация системы логирования"""
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _load_menu(self):
        """Загрузка меню из Google Sheets"""
        try:
            data = self.sheets.get_data(f"{Config.SHEET_NAME}!A2:D")
            if data:
                self.menu_manager = MenuManager(data)
                self.logger.info("Меню успешно загружено")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки меню: {e}")

    def _register_handlers(self):
        """Регистрация обработчиков сообщений"""
        @self.bot.message_handler(commands=['start', 'menu'])
        def handle_start(message: Message):
            self._show_root_menu(message.chat.id)

        @self.bot.message_handler(func=lambda m: True)
        def handle_message(message: Message):
            self._process_user_input(message)

    def _escape_markdown(self, text: str) -> str:
        """Экранирование специальных символов Markdown"""
        escape_chars = '_*[]()~`>#+-=|{}.!'
        return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

    def _format_content(self, item: MenuItem) -> str:
        """Форматирование контента с экранированием"""
        title = self._escape_markdown(item.title)
        text = self._escape_markdown(item.text) if item.text else ""
        return f"*{title}*\n\n{text}" if text else f"*{title}*"

    def _generate_keyboard(self, item: MenuItem) -> Optional[ReplyKeyboardMarkup]:
        """Генерация клавиатуры с учетом конечных пунктов"""
        buttons = []
    
        # Добавляем только если есть подпункты
        if item.children:
            buttons.extend([[child.title] for child in item.children])
    
        # Добавляем навигацию для всех пунктов кроме корневого
        if not item.is_root:
            nav_buttons = ["◀️ Назад"]
            if any(item.children):  # Если есть подпункты - добавляем "В начало"
                nav_buttons.append("🏠 В начало")
            buttons.append(nav_buttons)
    
        return self.keyboard_generator.create_reply_keyboard(buttons) if buttons else None

    def _show_root_menu(self, chat_id: int):
        """Отображение корневого меню"""
        if not self.menu_manager or not self.menu_manager.root_items:
            self.bot.send_message(chat_id, "⚠️ Меню временно недоступно")
            return
            
        self._show_menu(chat_id, self.menu_manager.root_items[0])

    def _show_menu(self, chat_id: int, menu_item: MenuItem):
        """Отображает пункт меню с корректным обновлением состояния"""
        try:
            # Всегда обновляем текущее состояние
            self.user_states[chat_id] = menu_item
        
            # Проверяем, является ли пункт конечным (нет подпунктов)
            if not menu_item.children and menu_item.text:
                # Конечный пункт - показываем только текст без клавиатуры
                self.bot.send_message(
                    chat_id,
                    self._format_content(menu_item),
                    parse_mode="MarkdownV2"
                )
                # Показываем навигационные кнопки отдельно
                nav_buttons = []
                if not menu_item.is_root:
                    nav_buttons = [["◀️ Назад", "🏠 В начало"]]
            
                if nav_buttons:
                    self.bot.send_message(
                        chat_id,
                        "Выберите действие:",
                        reply_markup=self.keyboard_generator.create_reply_keyboard(nav_buttons)
                    )
            else:
                # Обычный пункт меню - показываем с подпунктами
                keyboard = self._generate_keyboard(menu_item)
                self.bot.send_message(
                    chat_id,
                    self._format_content(menu_item),
                    reply_markup=keyboard,
                    parse_mode="MarkdownV2"
                )
            
        except Exception as e:
            self.logger.error(f"Ошибка отображения меню: {e}")
            # Фолбэк вариант
            self.bot.send_message(
                chat_id,
                f"{menu_item.title}\n\n{menu_item.text or ''}"
            )

    def _process_user_input(self, message: Message):
        """Обработка выбора пользователя"""
        chat_id = message.chat.id
        current_item = self.user_states.get(chat_id)
        
        if not current_item:
            self._show_root_menu(chat_id)
            return
            
        # Обработка навигации
        if message.text == "◀️ Назад":
            if parent := self.menu_manager.get_parent(current_item.id):
                self._show_menu(chat_id, parent)
            return
                
        if message.text == "🏠 В начало":
            self._show_root_menu(chat_id)
            return
            
        # Поиск выбранного пункта
        for child in current_item.children:
            if child.title == message.text:
                self._show_menu(chat_id, child)
                return
                
        self.bot.reply_to(message, "❌ Пункт не найден")

    def run(self):
        """Запуск бота"""
        self.logger.info("Запуск бота...")
        try:
            self.bot.infinity_polling()
        except Exception as e:
            self.logger.critical(f"Критическая ошибка: {e}")
        finally:
            self.logger.info("Бот остановлен")