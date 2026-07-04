from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


# Кнопки главного меню — появляются под полем ввода у пользователя
def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💰 Добавить запись"),
                KeyboardButton(text="📋 Мои записи"),
            ],
            [
                KeyboardButton(text="📊 Статистика"),
                KeyboardButton(text="💼 Бюджет"),
            ],
            [
                KeyboardButton(text="👨‍👩‍👧 Семья"),
                KeyboardButton(text="⚙️ Настройки"),
            ],
        ],
        resize_keyboard=True,      # подгоняет размер кнопок под экран
        input_field_placeholder="Выбери действие...",
    )


# Убрать клавиатуру (используется внутри диалогов)
def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
