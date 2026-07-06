"""
users.py — операции с пользователями

Пользователь идентифицируется по telegram_id.
Все функции используют соединение из connection.py.
"""

import time
from DB.connection import get_db


def get_user(telegram_id: int) -> dict | None:
    """
    Найти пользователя по telegram_id.
    Вернёт None если пользователь ещё не регистрировался.
    """
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (telegram_id,)
    ).fetchone()
    return dict(row) if row else None


def create_user(telegram_id: int, username: str | None, first_name: str) -> dict:
    """
    Создать нового пользователя при первом /start.
    Возвращает созданную запись.
    """
    db = get_db()
    db.execute(
        """
        INSERT INTO users (telegram_id, username, first_name, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (telegram_id, username, first_name, int(time.time()))
    )
    db.commit()
    return get_user(telegram_id)


def get_or_create_user(
    telegram_id: int,
    username: str | None,
    first_name: str
) -> tuple[dict, bool]:
    """
    Найти пользователя или создать если не существует.
    Возвращает (user, is_new).
    is_new = True если только что зарегистрировался.

    Использование в handlers/start.py:
        user, is_new = get_or_create_user(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
        )
    """
    user = get_user(telegram_id)
    if user:
        return user, False
    return create_user(telegram_id, username, first_name), True


def update_currency(telegram_id: int, currency: str) -> None:
    """Сохранить выбранную пользователем валюту."""
    db = get_db()
    db.execute(
        "UPDATE users SET default_currency = ? WHERE telegram_id = ?",
        (currency, telegram_id)
    )
    db.commit()


def update_notifications(telegram_id: int, enabled: bool) -> None:
    """Включить или выключить уведомления пользователя."""
    db = get_db()
    db.execute(
        "UPDATE users SET notifications = ? WHERE telegram_id = ?",
        (1 if enabled else 0, telegram_id)
    )
    db.commit()
