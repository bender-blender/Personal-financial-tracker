from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from DB.users import get_or_create_user
from DB.users import get_or_create_user

from keyboards.main_menu import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user, is_new = get_or_create_user(
    telegram_id=message.from_user.id,
    username=message.from_user.username,
    first_name=message.from_user.first_name,
    )  
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Я помогу тебе следить за доходами и расходами. "
        f"Добавляй траты, смотри статистику и планируй бюджет — "
        f"всё прямо в Telegram.\n\n"
        f"Выбери с чего начать 👇",
        reply_markup=main_menu_keyboard(),
    )


@router.message(Command("menu"))
async def cmd_menu(message: Message) -> None:
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_keyboard(),
    )