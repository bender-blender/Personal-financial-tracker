from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import CreateFamily, JoinFamily
from keyboards.key_sections import (
    stats_period_keyboard,
    budget_keyboard,
    family_main_keyboard, family_group_keyboard,
    settings_keyboard, currency_keyboard, notifications_keyboard,
)
from keyboards.main_menu import main_menu_keyboard

router = Router()


# ================================================================
# 📊 СТАТИСТИКА
# ================================================================

@router.message(F.text == "📊 Статистика")
async def btn_stats(message: Message) -> None:
    # TODO: Python-разработчик — подставить реальные данные из БД
    # данные ниже — заглушка для демонстрации визуала

    text = (
        "📊 *Статистика за этот месяц*\n\n"
        "💚 Доходы:  *0.00*\n"
        "❤️ Расходы: *0.00*\n"
        "💰 Баланс:  *0.00*\n\n"
        "Выбери период или тип графика:"
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=stats_period_keyboard())


@router.callback_query(F.data.startswith("stats:"))
async def stats_callback(callback: CallbackQuery) -> None:
    period = callback.data.split(":")[1]

    labels = {
        "week":        "эту неделю",
        "month":       "этот месяц",
        "year":        "этот год",
        "by_category": "категории",
        "dynamics":    "динамику",
    }

    # TODO: Python-разработчик — получить данные за period и сформировать текст/график
    await callback.answer(f"Загружаю данные за {labels.get(period, period)}...")
    await callback.message.edit_text(
        f"📊 *Статистика — {labels.get(period, period)}*\n\n"
        f"_Данные появятся когда Python-разработчик подключит БД_",
        parse_mode="Markdown",
        reply_markup=stats_period_keyboard(),
    )


# ================================================================
# 💼 БЮДЖЕТ
# ================================================================

def _progress_bar(current: int, limit: int, length: int = 10) -> str:
    """Рисует прогресс-бар из Unicode-блоков. Пример: ████░░░░░░ 40%"""
    if limit == 0:
        return "░" * length + " —"
    ratio = min(current / limit, 1.0)
    filled = round(ratio * length)
    bar = "█" * filled + "░" * (length - filled)
    percent = round(ratio * 100)
    emoji = "🔴" if ratio >= 1.0 else "🟡" if ratio >= 0.8 else "🟢"
    return f"{emoji} {bar} {percent}%"


@router.message(F.text == "💼 Бюджет")
async def btn_budget(message: Message) -> None:
    # TODO: Python-разработчик — заменить заглушки реальными данными из БД
    # Пример структуры данных которую ожидает этот хэндлер:
    # budgets = [
    #     {"name": "🍔 Еда",       "current": 3200, "limit": 5000},
    #     {"name": "🚗 Транспорт", "current": 1800, "limit": 2000},
    # ]

    budgets = []  # TODO: заполнить из БД

    if not budgets:
        text = (
            "💼 *Бюджет на этот месяц*\n\n"
            "Лимиты ещё не установлены.\n"
            "Нажми кнопку ниже чтобы задать лимит по категории."
        )
    else:
        lines = ["💼 *Бюджет на этот месяц*\n"]
        for b in budgets:
            bar = _progress_bar(b["current"], b["limit"])
            lines.append(
                f"{b['name']}\n"
                f"{bar}\n"
                f"_{b['current']:.2f} из {b['limit']:.2f}_\n"
            )
        text = "\n".join(lines)

    await message.answer(text, parse_mode="Markdown", reply_markup=budget_keyboard())


@router.callback_query(F.data == "budget:set")
async def budget_set(callback: CallbackQuery) -> None:
    # TODO: запустить FSM для установки лимита
    await callback.answer("Скоро здесь будет выбор категории и ввод лимита!")


@router.callback_query(F.data.in_({"budget:prev", "budget:next"}))
async def budget_month(callback: CallbackQuery) -> None:
    direction = "предыдущий" if callback.data == "budget:prev" else "следующий"
    # TODO: Python-разработчик — переключить месяц и перезагрузить данные
    await callback.answer(f"Переключаю на {direction} месяц...")


# ================================================================
# 👨‍👩‍👧 СЕМЬЯ
# ================================================================

@router.message(F.text == "👨‍👩‍👧 Семья")
async def btn_family(message: Message) -> None:
    # TODO: Python-разработчик — проверить через get_user_household(user_id)
    # есть ли у пользователя группа, и в зависимости от этого показать нужное меню
    in_group = False  # TODO: заменить реальной проверкой

    if not in_group:
        await message.answer(
            "👨‍👩‍👧 *Семейный бюджет*\n\n"
            "У тебя пока нет группы.\n\n"
            "Создай новую группу и пригласи семью по коду, "
            "или вступи в существующую группу.",
            parse_mode="Markdown",
            reply_markup=family_main_keyboard(),
        )
    else:
        # TODO: подставить реальное название группы
        await message.answer(
            "👨‍👩‍👧 *Семейный бюджет*\n\n"
            "Группа: *Название группы*\n"
            "Участников: *—*",
            parse_mode="Markdown",
            reply_markup=family_group_keyboard(),
        )


@router.callback_query(F.data == "family:create")
async def family_create(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(CreateFamily.waiting_name)
    await callback.message.edit_text(
        "👥 *Создание группы*\n\n"
        "Введи название группы:\n"
        "_Например: Семья Ивановых_",
        parse_mode="Markdown",
    )


@router.message(CreateFamily.waiting_name)
async def family_create_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    if len(name) < 2:
        await message.answer("⚠️ Название слишком короткое. Введи хотя бы 2 символа.")
        return

    # TODO: Python-разработчик — создать группу в БД и вернуть инвайт-код
    invite_code = "XXXX-YYYY"  # TODO: заменить реальным кодом из БД

    await state.clear()
    await message.answer(
        f"✅ *Группа «{name}» создана!*\n\n"
        f"🔑 Инвайт-код: `{invite_code}`\n\n"
        f"Поделись этим кодом с семьёй — они смогут вступить через меню «Семья».",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(F.data == "family:join")
async def family_join(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(JoinFamily.waiting_code)
    await callback.message.edit_text(
        "🔑 *Вход в группу*\n\n"
        "Введи инвайт-код который тебе прислали:",
        parse_mode="Markdown",
    )


@router.message(JoinFamily.waiting_code)
async def family_join_code(message: Message, state: FSMContext) -> None:
    code = message.text.strip().upper()

    # TODO: Python-разработчик — проверить код в БД и добавить пользователя в группу
    # если код неверный — вернуть ошибку
    code_valid = False  # TODO: заменить реальной проверкой

    if not code_valid:
        await message.answer(
            "⚠️ Код не найден или истёк срок действия.\n"
            "Проверь код и попробуй ещё раз."
        )
        return

    await state.clear()
    await message.answer(
        "✅ *Ты вступил в группу!*",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(F.data == "family:invite")
async def family_invite(callback: CallbackQuery) -> None:
    # TODO: Python-разработчик — получить инвайт-код группы из БД
    invite_code = "XXXX-YYYY"  # TODO: заменить реальным кодом
    await callback.message.answer(
        f"🔑 Инвайт-код твоей группы:\n\n`{invite_code}`\n\n"
        f"Перешли этот код тому кого хочешь пригласить.",
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "family:leave")
async def family_leave(callback: CallbackQuery) -> None:
    # TODO: Python-разработчик — убрать пользователя из группы в БД
    await callback.message.edit_text(
        "🚪 Ты вышел из группы.",
        reply_markup=family_main_keyboard(),
    )


@router.callback_query(F.data == "family:stats")
async def family_stats(callback: CallbackQuery) -> None:
    # TODO: Python-разработчик — загрузить статистику группы из БД
    await callback.message.edit_text(
        "📊 *Статистика группы*\n\n"
        "_Данные появятся когда Python-разработчик подключит БД_",
        parse_mode="Markdown",
        reply_markup=family_group_keyboard(),
    )


@router.callback_query(F.data == "family:members")
async def family_members(callback: CallbackQuery) -> None:
    # TODO: Python-разработчик — загрузить список участников из БД
    await callback.message.edit_text(
        "👤 *Участники группы:*\n\n"
        "_Список появится когда Python-разработчик подключит БД_",
        parse_mode="Markdown",
        reply_markup=family_group_keyboard(),
    )


# ================================================================
# ⚙️ НАСТРОЙКИ
# ================================================================

@router.message(F.text == "⚙️ Настройки")
async def btn_settings(message: Message) -> None:
    # TODO: Python-разработчик — загрузить текущие настройки пользователя из БД
    await message.answer(
        "⚙️ *Настройки*\n\n"
        "Валюта: *UAH*\n"
        "Уведомления: *включены*",
        parse_mode="Markdown",
        reply_markup=settings_keyboard(),
    )


@router.callback_query(F.data == "settings:currency")
async def settings_currency(callback: CallbackQuery) -> None:
    # TODO: Python-разработчик — передать текущую валюту пользователя
    current_currency = "UAH"  # TODO: загрузить из БД
    await callback.message.edit_text(
        "💱 *Выбери валюту:*",
        parse_mode="Markdown",
        reply_markup=currency_keyboard(current=current_currency),
    )


@router.callback_query(F.data.startswith("currency:"))
async def settings_currency_set(callback: CallbackQuery) -> None:
    code = callback.data.split(":")[1]
    # TODO: Python-разработчик — сохранить выбранную валюту в БД
    await callback.message.edit_text(
        f"✅ Валюта изменена на *{code}*",
        parse_mode="Markdown",
        reply_markup=settings_keyboard(),
    )


@router.callback_query(F.data == "settings:notifications")
async def settings_notifications(callback: CallbackQuery) -> None:
    # TODO: Python-разработчик — загрузить текущее состояние уведомлений из БД
    enabled = True  # TODO: загрузить из БД
    await callback.message.edit_text(
        "🔔 *Уведомления*\n\n"
        "Бот будет напоминать добавить запись если давно не было активности.",
        parse_mode="Markdown",
        reply_markup=notifications_keyboard(enabled=enabled),
    )


@router.callback_query(F.data.in_({"notifications:on", "notifications:off"}))
async def settings_notifications_toggle(callback: CallbackQuery) -> None:
    enabled = callback.data == "notifications:on"
    # TODO: Python-разработчик — сохранить состояние уведомлений в БД
    status = "включены" if enabled else "выключены"
    await callback.answer(f"Уведомления {status}")
    await callback.message.edit_reply_markup(
        reply_markup=notifications_keyboard(enabled=enabled)
    )


@router.callback_query(F.data == "settings:back")
async def settings_back(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "⚙️ *Настройки*",
        parse_mode="Markdown",
        reply_markup=settings_keyboard(),
    )
