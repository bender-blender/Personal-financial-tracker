import sqlite3
from pathlib import Path


# Глобальное соединение — создаётся один раз при старте бота
_connection: sqlite3.Connection | None = None


def init_db(db_path: str) -> None:
    """
    Инициализирует базу данных при старте бота.
    Создаёт таблицы если их нет.
    Вызывать один раз в main.py перед запуском polling.
    """
    global _connection

    _connection = sqlite3.connect(db_path, check_same_thread=False)
    _connection.row_factory = sqlite3.Row  # результаты как словари

    _connection.execute("PRAGMA foreign_keys = ON")
    _connection.execute("PRAGMA journal_mode = WAL")

    _apply_schema()


def get_db() -> sqlite3.Connection:
    """Возвращает активное соединение с БД."""
    if _connection is None:
        raise RuntimeError("База данных не инициализирована. Вызови init_db() в main.py")
    return _connection


def _apply_schema() -> None:
    """Применяет schema.sql если таблицы ещё не созданы."""
    schema_candidates = [
        Path(__file__).parent.parent / "schema.sql",
        Path(__file__).parent.parent.parent / "docs" / "schema.sql",
        Path(__file__).parent.parent.parent / "DB" / "schema.sql",
    ]

    for path in schema_candidates:
        if path.exists():
            sql = path.read_text(encoding="utf-8")
            _connection.executescript(sql)
            _connection.commit()
            return

    raise FileNotFoundError(
        "schema.sql не найден. Положи его рядом с папкой bot/ или в docs/"
    )
