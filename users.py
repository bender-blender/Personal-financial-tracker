import time
from .connection import get_db


def get_user(telegram_id: int) -> dict | None:
    """
    Возвращает пользователя по telegram_id.
    Возвращает None если пользователь не зарегистрирован.
    """
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE telegram_id = ?",
        (telegram_id,)
    ).fetchone()

    return dict(row) if row else None


def create_user(telegram_id: int, username: str | None, first_name: str) -> dict:
    """
    Создаёт нового пользователя при первом /start.
    Возвращает созданную запись.
    """
    db = get_db()
    now = int(time.time())

    db.execute(
        """
        INSERT INTO users (telegram_id, username, first_name, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (telegram_id, username, first_name, now)
    )
    db.commit()

    return get_user(telegram_id)


def get_or_create_user(telegram_id: int, username: str | None, first_name: str) -> tuple[dict, bool]:
    """
    Возвращает пользователя, создавая его если нужно.
    Возвращает (user, is_new) — второй элемент True если только что зарегистрировался.
    """
    user = get_user(telegram_id)
    if user:
        return user, False

    user = create_user(telegram_id, username, first_name)
    return user, True
