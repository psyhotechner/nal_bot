
from bot.bot import TelegramBot
import asyncio

if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.run())