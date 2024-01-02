import asyncio
import os
import random
import constants

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from db import db
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
user_message_count = {}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Саламчик маленькие, папа тут!")


@dp.message(F.text.lower() == "удалить")
async def delete_handler(message: Message) -> None:
    await db.delete_profile(message.from_user.id)


@dp.message(F.text.lower() == "z g m")
async def generate_meme(message: Message) -> None:
    photos = db.get_all_images()
    try:
        random_photo = random.choice(photos)
        random_index = photos.index(random_photo)
        words = db.get_all_words()
        size_of_meme = random.randint(0, len(words) - 1)
    except:
        await message.answer(constants.NO_INFORMATION_FOR_MEME)
    else:
        string_with_meme = ""
        for part in range(size_of_meme):
            string_with_meme += words[part] + " "
        await bot.send_photo(chat_id=message.chat.id, caption=string_with_meme, photo=photos[random_index])


@dp.message()
async def echo_handler(message: types.Message) -> None:
    user_id = message.from_user.id
    user_text = message.text
    photo = message.photo
    photo_url = ''
    if photo is None:
        photo_url = ""
    else:
        photo_url = photo[-1].file_id

    await db.fill_words_or_photos(user_id=user_id, word=user_text, photo=photo_url)

    try:
        words = db.get_all_words()
        size_of_meme = random.randint(0, len(words) - 1)
    except:
        await message.answer(constants.NO_INFORMATION_FOR_MEME)
    else:
        string_for_words = ""
        for word in range(size_of_meme):
            string_for_words += words[word] + " "
        user_id = message.from_user.id
        user_message_count[user_id] = user_message_count.get(user_id, 0) + 1
        if user_message_count[user_id] % 4 == 0:
            await message.reply(string_for_words)

    if db.size_of_db() > 250:
        await db.delete_db()


async def main() -> None:
    await db.db_start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
