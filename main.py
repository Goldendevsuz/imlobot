import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram.filters.command import Command
from dotenv import load_dotenv

from check_word import check_word
from transliterate import to_cyrillic

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv("BOT_TOKEN")

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.reply("uz_imlo Botiga Xush Kelibsiz!")

@dp.message(Command("help"))
async def command_start_handler(message: Message) -> None:
    await message.reply("Botdan foydalanish uchun so'z yuboring.")

@dp.message()
async def check_imlo(message: Message) -> None:
    word = message.text
    if word.isascii():
        word = to_cyrillic(word)

    result = check_word(word)
    if result['available']:
        response = f"✅\t{word.capitalize()}"
    else:
        response = f"❌\t{word.capitalize()}\n"
        for text in result['matches']:
            response += f"✅\t{text.capitalize()}\n"
    await message.answer(response)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
