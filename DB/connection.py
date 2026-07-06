"""
connection.py — подключение к SQLite для Telegram бота

Без пароля — Telegram сам авторизует пользователей.
Одно соединение на весь бот, создаётся при запуске в main.py.
"""

import sqlite3
from pathlib import Path

_connection: sqlite3.Connection | None = None


def init_db(db_path: str) -> None:
    """
    Вызвать один раз в main.py перед запуском бота.
    Создаёт таблицы если их ещё нет.
    """
    global _connection

    _connection = sqlite3.connect(db_path, check_same_thread=False)
    _connection.row_factory = sqlite3.Row  # результаты как словари

    _connection.execute("PRAGMA foreign_keys = ON")
    _connection.execute("PRAGMA journal_mode = WAL")

    _apply_schema()
    print(f"[DB] База данных инициализирована: {db_path}")


def get_db() -> sqlite3.Connection:
    """Возвращает активное соединение. Использовать в users.py и других модулях."""
    if _connection is None:
        raise RuntimeError(
            "База данных не инициализирована.\n"
            "Вызови init_db() в main.py перед запуском бота."
        )
    return _connection


def _apply_schema() -> None:
    """Ищет schema.sql и применяет его."""
    here = Path(__file__).parent
    candidates = [
        here / "schema.sql",
        here.parent / "schema.sql",
        here.parent / "docs" / "schema.sql",
    ]

    for path in candidates:
        if path.exists():
            sql = path.read_text(encoding="utf-8")
            _connection.executescript(sql)
            _connection.commit()
            print(f"[DB] Схема применена из {path}")
            return

    raise FileNotFoundError(
        "schema.sql не найден.\n"
        "Положи его рядом с connection.py или в папку docs/"
    )
