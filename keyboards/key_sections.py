from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# --- Бюджет ---

def budget_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Установить лимит", callback_data="budget:set")],
        [
            InlineKeyboardButton(text="◀️ Пред. месяц", callback_data="budget:prev"),
            InlineKeyboardButton(text="▶️ След. месяц", callback_data="budget:next"),
        ],
    ])


# --- Статистика ---

def stats_period_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Неделя",  callback_data="stats:week"),
            InlineKeyboardButton(text="Месяц",   callback_data="stats:month"),
            InlineKeyboardButton(text="Год",     callback_data="stats:year"),
        ],
        [
            InlineKeyboardButton(text="📊 По категориям", callback_data="stats:by_category"),
            InlineKeyboardButton(text="📈 Динамика",      callback_data="stats:dynamics"),
        ],
    ])


# --- Семья ---

def family_main_keyboard() -> InlineKeyboardMarkup:
    """Меню если пользователь НЕ в группе."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Создать группу",   callback_data="family:create")],
        [InlineKeyboardButton(text="🔑 Вступить по коду", callback_data="family:join")],
    ])


def family_group_keyboard() -> InlineKeyboardMarkup:
    """Меню если пользователь УЖЕ в группе."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика группы", callback_data="family:stats")],
        [InlineKeyboardButton(text="👤 Участники",         callback_data="family:members")],
        [InlineKeyboardButton(text="🔑 Инвайт-код",       callback_data="family:invite")],
        [InlineKeyboardButton(text="🚪 Выйти из группы",  callback_data="family:leave")],
    ])


# --- Настройки ---

def settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💱 Валюта",       callback_data="settings:currency")],
        [InlineKeyboardButton(text="🔔 Уведомления",  callback_data="settings:notifications")],
    ])


def currency_keyboard(current: str = "UAH") -> InlineKeyboardMarkup:
    """Выбор валюты. Текущая отмечена галочкой."""
    currencies = [
        ("🇺🇦 UAH", "UAH"),
        ("🇺🇸 USD", "USD"),
        ("🇪🇺 EUR", "EUR"),
        ("🇷🇺 RUB", "RUB"),
    ]

    rows = []
    for label, code in currencies:
        text = f"✅ {label}" if code == current else label
        rows.append([InlineKeyboardButton(text=text, callback_data=f"currency:{code}")])

    rows.append([InlineKeyboardButton(text="◀️ Назад", callback_data="settings:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def notifications_keyboard(enabled: bool = True) -> InlineKeyboardMarkup:
    status = "✅ Включены" if enabled else "❌ Выключены"
    toggle = "notifications:off" if enabled else "notifications:on"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=status, callback_data=toggle)],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="settings:back")],
    ])
