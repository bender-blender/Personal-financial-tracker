import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из папки проекта
load_dotenv(Path(__file__).parent / ".env")


def _require(key: str) -> str:
    """Достаёт переменную окружения. Падает с понятной ошибкой если нет."""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Переменная {key} не найдена.\n"
            f"Скопируй .env.example в .env и заполни значения."
        )
    return value


# Токен бота — обязательный
BOT_TOKEN: str = _require("BOT_TOKEN")

# Путь к базе данных
DB_PATH: str = os.getenv("DB_PATH", "finance.db")
