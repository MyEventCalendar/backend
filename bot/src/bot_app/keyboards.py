from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

inline_button_actual = InlineKeyboardButton('Actual events', callback_data='actual_events')
inline_button_today = InlineKeyboardButton('Events today', callback_data='today_events')
inline_kb = InlineKeyboardMarkup()

inline_kb.add(inline_button_actual)
inline_kb.add(inline_button_today)