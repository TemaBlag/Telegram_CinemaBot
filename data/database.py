import os
import aiosqlite
from pathlib import Path

DB_NAME = "bot.db"
DB_PATH = Path(DB_NAME)

async def init_db():
    """Создает таблицы, если их нет"""
    
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS film_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                film_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def log_search_query(user_id: int, query: str):
    """Сохраняет поисковый запрос пользователя"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO search_history (user_id, query) VALUES (?, ?)",
            (user_id, query)
        )
        await db.commit()

async def log_shown_movies(user_id: int, movies_list: list[dict]):
    """
    Сохраняет названия фильмов, которые были показаны пользователю.
    Принимает список словарей фильмов, которые вернул парсер.
    """
    if not movies_list:
        return
    data = [(user_id, movie['name']) for movie in movies_list]
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executemany(
            "INSERT INTO film_stats (user_id, film_name) VALUES (?, ?)",
            data
        )
        await db.commit()

async def get_user_history(user_id: int, limit: int = 10) -> list[tuple]:
    """
    Возвращает последние запросы пользователя.
    Результат: список кортежей (query, created_at)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT query, created_at 
            FROM search_history 
            WHERE user_id = ? 
            ORDER BY id DESC 
            LIMIT ?
            """,
            (user_id, limit)
        )
        rows = await cursor.fetchall()
        return rows

async def get_user_stats(user_id: int, limit: int = 10) -> list[tuple]:
    """
    Возвращает топ фильмов, которые чаще всего предлагались пользователю.
    Результат: список кортежей (film_name, count)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        query = """
            SELECT film_name, COUNT(*) as show_count
            FROM film_stats
            WHERE user_id = ?
            GROUP BY film_name
            ORDER BY show_count DESC
            LIMIT ?
        """
        cursor = await db.execute(query, (user_id, limit))
        rows = await cursor.fetchall()
        return rows