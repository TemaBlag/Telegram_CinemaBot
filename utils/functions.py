import aiohttp
import os
from urllib.parse import quote
from utils import parse_kinogo_html, prepare_telegram_response
from curl_cffi.requests import AsyncSession 

PROXY_URL = os.getenv("PROXY_URL")

def create_url(film_name: str) -> str:
    encoded_film_name: str = quote(film_name)
    return f"https://kinogo.ec/index.php?do=search&subaction=search&story={encoded_film_name}"

async def find_film(film_name: str) -> list[dict] | str:
    search_url: str = create_url(film_name)
    async with AsyncSession(impersonate="chrome", proxy=PROXY_URL) as session:
        try:
            response = await session.get(search_url)
            if response.status_code != 200:
                return f"❌ Сайт вернул ошибку: {response.status_code}"
            html_content = response.text 
            parsed_movies: list = parse_kinogo_html(html_content)
            return prepare_telegram_response(film_name, parsed_movies, top_films=3)
        except aiohttp.ClientError as e:
            return f"❌ Ошибка подключения: {e}"
        except Exception as e:
            return f"❌ Произошла непредвиденная ошибка: {e}"