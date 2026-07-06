"""
db_transactions.py — сохранение и получение транзакций из БД

Использование в handlers/transactions.py:
    from db_transactions import save_transaction, get_transactions, get_stats
"""

import time
from DB.connection import get_db

# Соответствие callback_data → category_id из таблицы categories
CATEGORY_MAP = {
    "food":         1,
    "transport":    2,
    "home":         3,
    "health":       4,
    "entertainment":5,
    "clothes":      6,
    "education":    7,
    "other":        8,
    "salary":       9,
    "freelance":    10,
    "gift":         11,
    "other_income": 12,
}


def save_transaction(
    telegram_id: int,
    amount: float,
    transaction_type: str,
    category_key: str,
    note: str | None = None,
) -> bool:
    """
    Сохраняет транзакцию в БД.

    amount          — сумма в рублях/гривнах (15.50), конвертируем в копейки
    transaction_type — 'income' или 'expense'
    category_key    — ключ из CATEGORY_MAP ('food', 'salary' и т.д.)

    Возвращает True если сохранено успешно.
    """
    db = get_db()

    # Получаем user_id по telegram_id
    user = db.execute(
        "SELECT id, default_currency FROM users WHERE telegram_id = ?",
        (telegram_id,)
    ).fetchone()

    if not user:
        return False

    amount_kopecks = round(amount * 100)  # переводим в копейки
    category_id = CATEGORY_MAP.get(category_key, 8)  # 8 = "Прочее" если не найдено
    now = int(time.time())

    db.execute(
        """
        INSERT INTO transactions
            (user_id, amount, currency, category_id, type, date, note, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user["id"], amount_kopecks, user["default_currency"],
         category_id, transaction_type, now, note, now)
    )
    db.commit()
    return True


def get_transactions(telegram_id: int, period: str = "month") -> list[dict]:
    """
    Возвращает список транзакций пользователя за период.
    period: 'week' | 'month' | 'all'
    """
    db = get_db()
    now = int(time.time())

    if period == "week":
        date_from = now - 7 * 24 * 3600
    elif period == "month":
        date_from = now - 30 * 24 * 3600
    else:
        date_from = 0  # все записи

    rows = db.execute(
        """
        SELECT
            t.amount,
            t.type,
            t.date,
            t.note,
            c.name  AS category_name,
            t.currency
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        JOIN categories c ON t.category_id = c.id
        WHERE u.telegram_id = ?
          AND t.date >= ?
        ORDER BY t.date DESC
        LIMIT 50
        """,
        (telegram_id, date_from)
    ).fetchall()

    result = []
    for row in rows:
        import datetime
        dt = datetime.datetime.utcfromtimestamp(row["date"])
        result.append({
            "amount":        row["amount"] / 100,         # обратно в рубли/гривны
            "type":          row["type"],
            "date":          dt.strftime("%d.%m"),
            "category_name": row["category_name"],
            "note":          row["note"] or "",
            "currency":      row["currency"],
        })
    return result


def get_stats(telegram_id: int, period: str = "month") -> dict:
    """
    Возвращает сводную статистику за период.
    Результат:
    {
        "income":   1500.00,
        "expense":  900.00,
        "balance":  600.00,
        "currency": "UAH",
        "by_category": [
            {"name": "Еда", "total": 450.00, "type": "expense"},
            ...
        ]
    }
    """
    db = get_db()
    now = int(time.time())

    if period == "week":
        date_from = now - 7 * 24 * 3600
    elif period == "month":
        date_from = now - 30 * 24 * 3600
    else:
        date_from = 0

    # Общие суммы доходов и расходов
    totals = db.execute(
        """
        SELECT
            t.type,
            SUM(t.amount) AS total
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        WHERE u.telegram_id = ?
          AND t.date >= ?
        GROUP BY t.type
        """,
        (telegram_id, date_from)
    ).fetchall()

    income  = 0
    expense = 0
    for row in totals:
        if row["type"] == "income":
            income = row["total"] / 100
        else:
            expense = row["total"] / 100

    # По категориям
    by_category = db.execute(
        """
        SELECT
            c.name,
            c.type,
            SUM(t.amount) AS total
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        JOIN categories c ON t.category_id = c.id
        WHERE u.telegram_id = ?
          AND t.date >= ?
        GROUP BY c.id
        ORDER BY total DESC
        """,
        (telegram_id, date_from)
    ).fetchall()

    # Валюта пользователя
    user = db.execute(
        "SELECT default_currency FROM users WHERE telegram_id = ?",
        (telegram_id,)
    ).fetchone()
    currency = user["default_currency"] if user else "UAH"

    return {
        "income":      income,
        "expense":     expense,
        "balance":     income - expense,
        "currency":    currency,
        "by_category": [
            {"name": r["name"], "total": r["total"] / 100, "type": r["type"]}
            for r in by_category
        ],
    }
