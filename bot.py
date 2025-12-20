from aiogram import Bot, Dispatcher
from aiogram.filters import Command
import os
from dotenv import load_dotenv
import asyncio
from aiogram.types import Message
from utils import find_film
from aiogram.client.session.aiohttp import AiohttpSession
from data import (
    init_db, 
    log_search_query, 
    log_shown_movies, 
    get_user_history, 
    get_user_stats
)


PROXY_URL = os.getenv("PROXY_URL")

session = AiohttpSession(proxy=PROXY_URL)

BOT_TOKEN = os.getenv("BOT_TOKEN", session=session)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    text = """🎬 **Добро пожаловать в MovieFinder Bot!**

Я — ваш олдскульный AI-ассистент, который поможет быстро и удобно находить фильмы и сериалы.
Я могу показать краткую информацию о фильме, его постер, рейтинг и даже дать прямые ссылки для просмотра.

✨ **Что я умею:**
/history — Просмотреть историю ваших запросов
/stats — Узнать, как часто вам предлагался каждый фильм
/help — Инструкции и подсказки по работе с ботом

Просто введите название фильма — и получите всю нужную информацию.
Давайте сделаем ваш вечер ещё приятнее! 🍿"""
    
    await message.answer(text, parse_mode="Markdown")

@dp.message(Command("help"))
async def help_handler(message: Message):
    text = """❓ **Как пользоваться CinemaBot:**

Просто введите название фильма или сериала — и я найду для вас всю необходимую информацию, включая:
• Постер
• Рейтинг
• Краткое описание
• Прямые ссылки для просмотра

**Другие полезные команды:**
/history — Просмотреть вашу личную историю запросов
/stats — Узнать, как часто вам предлагался каждый фильм

Приятного просмотра и интересных открытий! 🍿"""

    await message.answer(text, parse_mode="Markdown")

@dp.message(Command("history"))
async def history_handler(message: Message):
    user_id = message.from_user.id
    history = await get_user_history(user_id, limit=20)
    if not history:
        await message.answer("📜 Ваша история поиска пуста.", parse_mode="Markdown")
        return
    text_lines = ["📜 **Ваша история поиска (последние 20):**\n"]
    for query, created_at in history:
        text_lines.append(f"🕒 `{created_at}` — **{query}**")
    await message.answer("\n".join(text_lines), parse_mode="Markdown")

@dp.message(Command("stats"))
async def stats_handler(message: Message):
    user_id = message.from_user.id
    stats = await get_user_stats(user_id, limit=10)
    if not stats:
        await message.answer("📊 Статистики пока нет. Начните искать фильмы!", parse_mode="Markdown")
        return
    text_lines = ["📊 **Топ фильмов, которые мы вам предлагали:**\n"]
    for i, (film_name, count) in enumerate(stats, 1):
        text_lines.append(f"{i}. 🎬 **{film_name}** — {count} раз(а)")
    await message.answer("\n".join(text_lines), parse_mode="Markdown")

@dp.message()
async def query_handler(message: Message):
    user_id = message.from_user.id
    if message.text is None or message.text.startswith("/"):
        return
    
    film_name: str = message.text

    await log_search_query(user_id, film_name)

    messages_to_send = await find_film(film_name)
    if isinstance(messages_to_send, str):
        await bot.send_message(user_id, messages_to_send)
        return

    if not messages_to_send:
        await bot.send_message(user_id, "Пока не удалось найти фильмы с таким названием. Попробуйте посмотреть другой фильм! 🙂")
    else:
        try:
            await log_shown_movies(user_id, messages_to_send)
        except KeyError:
            print("ОШИБКА: В словаре фильма нет ключа 'name'. Проверьте utils.py!")
        except Exception as e:
            print(f"Ошибка записи статистики: {e}")
        for msg in messages_to_send:
            try:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=msg['photo'],
                    caption=msg['caption'],
                    parse_mode=msg['parse_mode']
                )
                await asyncio.sleep(0.5) 
                
            except Exception as e:
                print(f"Ошибка отправки: {e}")
                await bot.send_message(user_id, msg['caption'], parse_mode=msg['parse_mode'])

async def main():
    await init_db()
    print("Bot is online...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
