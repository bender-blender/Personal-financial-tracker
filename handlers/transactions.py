from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from states import AddTransaction
from keyboards.key_transactions import (
    type_keyboard, category_keyboard,
    note_keyboard, confirm_keyboard,
)
from keyboards.main_menu import main_menu_keyboard

router = Router()

# Словари для красивого отображения
TYPE_LABELS = {"income": "💚 Доход", "expense": "❤️ Расход"}
CATEGORY_LABELS = {
    "food":         "🍔 Еда",
    "transport":    "🚗 Транспорт",
    "home":         "🏠 Жильё",
    "health":       "💊 Здоровье",
    "entertainment":"🎮 Развлечения",
    "clothes":      "👕 Одежда",
    "education":    "📚 Образование",
    "other":        "📦 Прочее",
    "salary":       "💼 Зарплата",
    "freelance":    "💻 Фриланс",
    "gift":         "🎁 Подарок",
    "other_income": "📦 Прочее",
}


# --- Шаг 1: запрашиваем сумму ---

@router.message(F.text == "💰 Добавить запись")
async def btn_add(message: Message, state: FSMContext) -> None:
    await state.set_state(AddTransaction.amount)
    await message.answer(
        "💰 *Добавление записи*\n\n"
        "Введи сумму:\n"
        "_Например: 150 или 1500.50_",
        parse_mode="Markdown",
    )


# --- Шаг 2: получаем сумму, спрашиваем тип ---

@router.message(AddTransaction.amount)
async def step_amount(message: Message, state: FSMContext) -> None:
    # Валидация суммы
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.answer(
            "⚠️ Введи корректную сумму — только число больше нуля.\n"
            "_Например: 150 или 1500.50_",
            parse_mode="Markdown",
        )
        return

    await state.update_data(amount=amount)
    await state.set_state(AddTransaction.type)

    await message.answer(
        f"✅ Сумма: *{amount:.2f}*\n\n"
        f"Это доход или расход?",
        parse_mode="Markdown",
        reply_markup=type_keyboard(),
    )


# --- Шаг 3: получаем тип, спрашиваем категорию ---

@router.callback_query(AddTransaction.type, F.data.startswith("type:"))
async def step_type(callback: CallbackQuery, state: FSMContext) -> None:
    transaction_type = callback.data.split(":")[1]
    await state.update_data(type=transaction_type)
    await state.set_state(AddTransaction.category)

    await callback.message.edit_text(
        f"✅ Тип: *{TYPE_LABELS[transaction_type]}*\n\n"
        f"Выбери категорию:",
        parse_mode="Markdown",
        reply_markup=category_keyboard(transaction_type),
    )


# --- Шаг 4: получаем категорию, спрашиваем заметку ---

@router.callback_query(AddTransaction.category, F.data.startswith("cat:"))
async def step_category(callback: CallbackQuery, state: FSMContext) -> None:
    category = callback.data.split(":")[1]
    await state.update_data(category=category)
    await state.set_state(AddTransaction.note)

    await callback.message.edit_text(
        f"✅ Категория: *{CATEGORY_LABELS[category]}*\n\n"
        f"Добавь заметку или пропусти:",
        parse_mode="Markdown",
        reply_markup=note_keyboard(),
    )


# --- Шаг 5а: пользователь написал заметку ---

@router.message(AddTransaction.note)
async def step_note_text(message: Message, state: FSMContext) -> None:
    await state.update_data(note=message.text)
    await _show_confirm(message, state)


# --- Шаг 5б: пользователь нажал "Пропустить" ---

@router.callback_query(AddTransaction.note, F.data == "skip_note")
async def step_note_skip(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(note=None)
    await _show_confirm(callback.message, state)


# --- Шаг 6: показываем итог ---

async def _show_confirm(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    note_line = f"📝 Заметка: {data['note']}" if data.get("note") else ""

    text = (
        f"📋 *Проверь данные:*\n\n"
        f"💰 Сумма: *{data['amount']:.2f}*\n"
        f"{'💚' if data['type'] == 'income' else '❤️'} Тип: *{TYPE_LABELS[data['type']]}*\n"
        f"📂 Категория: *{CATEGORY_LABELS[data['category']]}*\n"
        + (f"📝 Заметка: _{data['note']}_\n" if data.get("note") else "")
        + f"\nВсё верно?"
    )

    await state.set_state(AddTransaction.confirm)
    await message.answer(text, parse_mode="Markdown", reply_markup=confirm_keyboard())


# --- Шаг 7: сохраняем или отменяем ---

@router.callback_query(AddTransaction.confirm, F.data == "confirm")
async def step_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()

    # TODO: Python-разработчик — вызвать здесь функцию сохранения в БД
    # например: await save_transaction(user_id=callback.from_user.id, **data)

    await state.clear()
    await callback.message.edit_text(
        f"✅ *Запись сохранена!*\n\n"
        f"{TYPE_LABELS[data['type']]} на *{data['amount']:.2f}* — {CATEGORY_LABELS[data['category']]}",
        parse_mode="Markdown",
    )
    await callback.message.answer("Что дальше?", reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "cancel")
async def step_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("❌ Отменено.")
    await callback.message.answer("Главное меню:", reply_markup=main_menu_keyboard())
