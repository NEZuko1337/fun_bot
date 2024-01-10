import asyncio
import os
import random

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv

from bot import constants, text_to_speech
from db import db

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
user_message_count = {}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(constants.GREETINGS)


@dp.message(F.text.lower() == "удалить")
async def delete_handler(message: Message) -> None:
    await db.delete_profile(message.from_user.id)


@dp.message(F.text.lower() == "z g m")
async def generate_meme(message: Message) -> None:
    try:
        photos = db.get_all_images()
        random_photo = random.choice(photos)
        random_index = photos.index(random_photo)
        words = db.get_all_words()
    except:
        await message.answer(constants.NO_INFORMATION_FOR_MEME)
    else:
        size_of_meme = random.randint(1, 20)
        string_with_meme = ""
        for _ in range(size_of_meme):
            string_with_meme += random.choice(words) + " "
        await bot.send_photo(chat_id=message.chat.id, caption=string_with_meme, photo=photos[random_index])


@dp.message(F.text.lower() == "z g a")
async def generate_answer_with_audio(message: Message) -> None:
    try:
        words = db.get_all_words()
        size_of_syntax = random.randint(1, 20)
    except:
        await message.answer(constants.NO_INFORMATION_FOR_MEME)
    else:
        string_for_words = ""
        for word in range(size_of_syntax):
            string_for_words += random.choice(words) + " "

        filepath = text_to_speech.convert_text_to_speech(text=string_for_words)
        voice = FSInputFile(path=filepath)
        await message.reply_audio(voice)


@dp.message(F.text.lower() == "обновление")
async def say_about_new_update(message: Message) -> None:
    if message.from_user.id == 666729461:
        filename = "update.opus"
        if filename not in os.listdir("AUDIO"):
            text_to_speech.update_info()

        update_voice = FSInputFile(path="AUDIO/update.opus")
        await message.reply_audio(audio=update_voice, caption=constants.UPDATE1_INPUT)
    else:
        await message.reply(text=constants.DONT_HAVE_PERMISSIONS)


@dp.message(F.text.lower() == "очистить")
async def del_db(message: Message) -> None:
    if message.from_user.id == 666729461:
        await db.delete_db()
    else:
        await message.reply(text=constants.DONT_HAVE_PERMISSIONS)


@dp.message()
async def echo_handler(message: Message) -> None:
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
        size_of_meme = random.randint(1, 20)
    except:
        await message.answer(constants.NO_INFORMATION_FOR_MEME)
    else:
        string_for_words = ""
        for word in range(size_of_meme):
            string_for_words += random.choice(words) + " "
        user_id = message.from_user.id
        user_message_count[user_id] = user_message_count.get(user_id, 0) + 1
        if user_message_count[user_id] % 4 == 0:
            await message.reply(string_for_words)

    if db.size_of_db() > 400:
        await db.delete_db()


async def main() -> None:
    await db.db_start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
