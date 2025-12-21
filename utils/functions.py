import aiohttp
from urllib.parse import quote
from utils import parse_kinogo_html, prepare_telegram_response

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://kinogo.ec/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
}

def create_url(film_name: str) -> str:
    encoded_film_name: str = quote(film_name)
    return f"https://kinogo.ec/index.php?do=search&subaction=search&story={encoded_film_name}"

async def find_film(film_name: str) -> list[dict] | str:
    search_url: str = create_url(film_name)
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(search_url) as response:
                if response.status != 200:
                    return f"❌ Сайт вернул ошибку: {response.status}"
                html_content: str = await response.text()
                parsed_movies: list = parse_kinogo_html(html_content)
                return prepare_telegram_response(film_name, parsed_movies, top_films=3)
        except aiohttp.ClientError as e:
            return f"❌ Ошибка подключения: {e}"
        except Exception as e:
            return f"❌ Произошла непредвиденная ошибка: {e}"
