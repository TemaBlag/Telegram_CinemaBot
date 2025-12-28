# 🎬 CinemaBot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat\&logo=python)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blueviolet?style=flat\&logo=telegram)
![License](https://img.shields.io/badge/License-MIT-green)

**CinemaBot** is a fast and user-friendly Telegram bot for searching movies and TV shows.
It is fully asynchronous, parses data from popular cinema websites in real time, and maintains personalized statistics for each user.

[![Telegram Bot](https://img.shields.io/badge/Telegram-Start_Bot-2CA5E0?style=for-the-badge\&logo=telegram\&logoColor=white)](https://t.me/ThisIsBestCinemaBot)

---

## ✨ Features

* 🚀 **Fully asynchronous:** Built with `aiogram` and `aiohttp` for instant, non-blocking responses.
* 🔍 **Live search:** Real-time parsing of results from Kinogo (or similar websites) using `BeautifulSoup4`.
* 📊 **Database:** Stores search history and query statistics in `SQLite` via `aiosqlite`.
* 🛡 **Anti-bot bypass:** Mimics a real browser (User-Agent) to ensure successful parsing.
* 📱 **User-friendly interface:** Clean message formatting (Markdown) and tidy links.

## 🛠 Tech Stack

* **Language:** Python 3.10+
* **Telegram API:** [aiogram 3.x](https://docs.aiogram.dev/)
* **HTTP client:** [aiohttp](https://docs.aiohttp.org/)
* **Parsing:** [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) + [lxml](https://lxml.de/)
* **Database:** [aiosqlite](https://github.com/omnilib/aiosqlite)
* **Configuration:** [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## ⚙️ Installation & Run

Follow these steps to deploy the bot locally or on a server.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cinemabot.git
cd cinemabot
```

### 2. Create a virtual environment

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your credentials:

```env
BOT_TOKEN=your_bot_token_from_BotFather
```

### 5. Run the bot

```bash
python bot.py
```

---

## 🤖 Bot Commands

| Command    | Description                              |
| :--------- | :--------------------------------------- |
| `/start`   | Start the bot and show a welcome message |
| `/help`    | Display usage instructions               |
| `/history` | Show the last 5 search queries           |
| `/stats`   | Show the top 5 most frequent queries     |
| **Text**   | Send a movie or TV show title to search  |
