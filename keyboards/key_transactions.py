from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def type_keyboard() -> InlineKeyboardMarkup:
    """Выбор типа: доход или расход."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💚 Доход",  callback_data="type:income"),
            InlineKeyboardButton(text="❤️ Расход", callback_data="type:expense"),
        ]
    ])


def category_keyboard(transaction_type: str) -> InlineKeyboardMarkup:
    """Категории в зависимости от типа транзакции."""
    if transaction_type == "expense":
        buttons = [
            ("🍔 Еда",          "cat:food"),
            ("🚗 Транспорт",    "cat:transport"),
            ("🏠 Жильё",        "cat:home"),
            ("💊 Здоровье",     "cat:health"),
            ("🎮 Развлечения",  "cat:entertainment"),
            ("👕 Одежда",       "cat:clothes"),
            ("📚 Образование",  "cat:education"),
            ("📦 Прочее",       "cat:other"),
        ]
    else:
        buttons = [
            ("💼 Зарплата",     "cat:salary"),
            ("💻 Фриланс",      "cat:freelance"),
            ("🎁 Подарок",      "cat:gift"),
            ("📦 Прочее",       "cat:other_income"),
        ]

    # Раскладываем по 2 кнопки в ряд
    rows = []
    for i in range(0, len(buttons), 2):
        row = [InlineKeyboardButton(text=b[0], callback_data=b[1]) for b in buttons[i:i+2]]
        rows.append(row)

    rows.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def note_keyboard() -> InlineKeyboardMarkup:
    """Предложение пропустить заметку."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Пропустить", callback_data="skip_note")],
        [InlineKeyboardButton(text="❌ Отмена",      callback_data="cancel")],
    ])


def confirm_keyboard() -> InlineKeyboardMarkup:
    """Подтверждение или отмена сохранения."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Сохранить", callback_data="confirm"),
            InlineKeyboardButton(text="❌ Отмена",    callback_data="cancel"),
        ]
    ])


def records_filter_keyboard() -> InlineKeyboardMarkup:
    """Фильтры для списка записей."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="За неделю",  callback_data="filter:week"),
            InlineKeyboardButton(text="За месяц",   callback_data="filter:month"),
            InlineKeyboardButton(text="Всё время",  callback_data="filter:all"),
        ],
        [InlineKeyboardButton(text="📂 По категории", callback_data="filter:category")],
    ])
