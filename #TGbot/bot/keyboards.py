from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List, Optional, Dict, Any

class KeyboardGenerator:
    @staticmethod
    def create_reply_keyboard(buttons: List[List[str]], **kwargs) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(
            resize_keyboard=kwargs.get('resize_keyboard', True),
            one_time_keyboard=kwargs.get('one_time_keyboard', False)
        )
        
        for row in buttons:
            markup.row(*[KeyboardButton(btn) for btn in row])
        
        return markup