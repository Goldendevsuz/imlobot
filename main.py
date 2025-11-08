import aiohttp
import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

import requests
from dotenv import load_dotenv

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN", "your bot token")
API_KEY = getenv("API_KEY", "your weather token")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

async def get_temp(city):

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric") as response:
            data = await response.json()

            if data.get("cod") == 200:
                return data["main"].get("temp")



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def weather_handler(message: Message) -> None:
    try:
        temp = await get_temp(message.text)
        if temp:
            await message.reply(f"{temp}℃")
        else:
            await message.reply("City not found")

    except TypeError:
        await message.reply("Exception was occured")
    
    return 


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())