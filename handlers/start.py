from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards.main_menu import main_menu_keyboard  # ← добавить

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Я помогу тебе следить за доходами и расходами.\n\n"
        f"Выбери с чего начать 👇",
        reply_markup=main_menu_keyboard(),
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())


@router.message(lambda m: m.text == "💰 Добавить запись")
async def btn_add(message: Message) -> None:
    await message.answer("📝 Раздел в разработке — скоро будет!")


@router.message(lambda m: m.text == "📋 Мои записи")
async def btn_list(message: Message) -> None:
    await message.answer("📋 Раздел в разработке — скоро будет!")


@router.message(lambda m: m.text == "📊 Статистика")
async def btn_stats(message: Message) -> None:
    await message.answer("📊 Раздел в разработке — скоро будет!")


@router.message(lambda m: m.text == "💼 Бюджет")
async def btn_budget(message: Message) -> None:
    await message.answer("💼 Раздел в разработке — скоро будет!")


@router.message(lambda m: m.text == "👨‍👩‍👧 Семья")
async def btn_family(message: Message) -> None:
    await message.answer("👨‍👩‍👧 Раздел в разработке — скоро будет!")


@router.message(lambda m: m.text == "⚙️ Настройки")
async def btn_settings(message: Message) -> None:
    await message.answer("⚙️ Раздел в разработке — скоро будет!")