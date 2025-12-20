from bs4 import BeautifulSoup
import re
import difflib

def parse_kinogo_html(html_source: str) -> list[dict[str, str]]:
    """
    Из полученного html страницы создаётся список опсаний фильма:
    'name': имя фильма
    'year': год выпуска фильма
    'description': описание фильма
    'rating': рэйтинг фильма
    'image': превью
    'link': ссылка для просмотра
    """
    soup = BeautifulSoup(html_source, 'lxml')
    base_url: str = "https://kinogo.ec"
    results: list[dict[str, str]] = []
    items = soup.find_all('div', class_='shortstory')

    for item in items:
        try:
            header = item.find('div', class_='shortstory__title')
            link_tag = header.find('a')
            name = link_tag.get_text(strip=True)
            link = link_tag['href']
            poster_div = item.find('div', class_='shortstory__poster')
            img_tag = poster_div.find('img')
            img_rel_path = img_tag.get('data-src') or img_tag.get('src')
            if img_rel_path and img_rel_path.startswith('/'):
                image = base_url + img_rel_path
            else:
                image = img_rel_path
            excerpt_div = item.find('div', class_='excerpt')
            description = excerpt_div.get_text(strip=True) if excerpt_div else "Описание отсутствует"
            info_div = item.find('div', class_='shortstory__info')
            year = "Не указан"
            year_label = info_div.find('b', string="Год выпуска:")
            if year_label:
                year_link = year_label.find_next('a')
                if year_link:
                    year = year_link.get_text(strip=True)
            ratings = []
            kp = info_div.find('span', class_='kp')
            imdb = info_div.find('span', class_='imdb')
            if kp:
                ratings.append(kp.get_text(strip=True))
            if imdb:
                ratings.append(imdb.get_text(strip=True))
            rating_str = ", ".join(ratings) if ratings else "Нет рейтинга"
            movie_data = {
                'name': name,
                'year': year,
                'description': description,
                'rating': rating_str,
                'image': image,
                'link': link
            }
            results.append(movie_data)
        except Exception as e:
            print(f"Ошибка парсинга элемента: {e}")
            continue
    return results

def remove_parentheses(text: str) -> str:
    """
    Удаляет круглые скобки и всё содержимое внутри них.
    Пример: "It (2017)" -> "It"
    """
    return re.sub(r"\s*\([^)]*\)", "", text.lower()).strip()


def prepare_telegram_response(film_name: str, movies_list: list[dict[str, str]], top_films: int):
    """
    Принимает список словарей фильмов.
    Возвращает список готовых объектов для отправки (фото + текст).
    """
    norm_query_loop: str = remove_parentheses(film_name)
    find_best_movie: bool = False
    best_matches: list[dict[str, str]] = []

    for movie in movies_list:
        movie_name_norm = remove_parentheses(movie['name'].lower())
        if movie_name_norm == norm_query_loop:
            best_matches.append(movie)
            find_best_movie = True
            break
    if not find_best_movie:
        scores: list[tuple[float, dict[str, str]]] = []
        for movie in movies_list:
            name = remove_parentheses(movie['name'])
            similarity = difflib.SequenceMatcher(None, norm_query_loop, name).ratio()
            scores.append((similarity, movie))
        scores.sort(key=lambda x: x[0], reverse=True)

        for score_tuple in scores[:top_films]:
            best_matches.append(score_tuple[1])

    prepared_messages: list[dict[str, str]] = []

    for movie in best_matches:
        caption: str = f"🎬 <b>{movie['name']}</b>\n\n"
        caption += f"⭐️ <b>Рейтинг:</b> {movie['rating']}\n"
        desc: str = movie.get('description', 'Описание отсутствует.')
        if len(desc) > 300:
            desc = desc[:300].strip() + "..."
        caption += f"📝 <b>Описание:</b> {desc}\n\n"

        caption += f"▶️ <a href='{movie['link']}'>Смотреть фильм онлайн</a>"
        message_data: dict[str, str] = {
            'photo': movie['image'],
            'caption': caption,
            'parse_mode': 'HTML',
            'name': movie['name']
        }
        prepared_messages.append(message_data)

    return prepared_messages