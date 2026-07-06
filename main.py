import asyncio
import logging
from DB.connection import init_db

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import start
from handlers import transactions
from handlers import records
from handlers import sections


async def main() -> None:
    init_db(config.DB_PATH)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    log = logging.getLogger(__name__)

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Порядок важен — start первым, потом остальные
    dp.include_router(start.router)
    dp.include_router(transactions.router)
    dp.include_router(records.router)
    dp.include_router(sections.router)

    log.info("Бот запущен. Жду сообщений...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())