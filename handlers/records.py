from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.key_transactions import records_filter_keyboard
from keyboards.main_menu import main_menu_keyboard

router = Router()


@router.message(F.text == "📋 Мои записи")
async def btn_records(message: Message) -> None:
    # TODO: Python-разработчик — загрузить последние транзакции из БД
    # Пример структуры данных:
    # records = [
    #     {"date": "04.07", "type": "expense", "amount": 250.0, "category": "🍔 Еда",       "note": "обед"},
    #     {"date": "04.07", "type": "income",  "amount": 5000.0,"category": "💼 Зарплата",  "note": ""},
    # ]

    records = []  # TODO: заменить реальными данными

    if not records:
        text = (
            "📋 *Мои записи*\n\n"
            "Записей пока нет.\n"
            "Нажми *«💰 Добавить запись»* чтобы начать!"
        )
    else:
        lines = ["📋 *Мои записи за месяц:*\n"]
        for r in records:
            sign  = "➕" if r["type"] == "income" else "➖"
            note  = f" — {r['note']}" if r.get("note") else ""
            lines.append(f"{r['date']} {sign} *{r['amount']:.2f}* {r['category']}{note}")
        text = "\n".join(lines)

    await message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=records_filter_keyboard(),
    )


@router.callback_query(F.data.startswith("filter:"))
async def records_filter(callback: CallbackQuery) -> None:
    period = callback.data.split(":")[1]
    labels = {
        "week":     "эту неделю",
        "month":    "этот месяц",
        "all":      "всё время",
        "category": "выбранную категорию",
    }
    # TODO: Python-разработчик — загрузить записи за нужный period из БД
    await callback.answer(f"Фильтр: {labels.get(period, period)}")
    await callback.message.edit_text(
        f"📋 *Записи за {labels.get(period, period)}:*\n\n"
        f"_Данные появятся когда Python-разработчик подключит БД_",
        parse_mode="Markdown",
        reply_markup=records_filter_keyboard(),
    )
