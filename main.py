from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from bot.handlers import router
from bot.config import BOT_TOKEN


# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage() 
dp = Dispatcher(storage=storage)

async def main():
    """
    Функция для настройки и запуска бота.

    Эта функция включает роутер, очищает webhook (если он был установлен),
    и запускает процесс polling для получения обновлений.
    """
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
