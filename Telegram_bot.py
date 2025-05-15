import asyncio
import aiosqlite
from telethon import TelegramClient, events

# Замените на свои данные
api_id = 123456  # <-- Твой API ID
api_hash = 'your_api_hash_here'
session_name = 'userbot_session'  # имя файла сессии

client = TelegramClient(session_name, api_id, api_hash)

# Монеты
crypto_coins = ['Bitcoin', 'Ethereum', 'BNB', 'Solana', 'XRP']
meme_coins = ['Dogecoin', 'Shiba Inu', 'Pepe', 'Floki', 'Bonk']
all_coins = crypto_coins + meme_coins


# Инициализация базы
async def init_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_choices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                choices TEXT
            )
        ''')
        await db.commit()


# Отправка сообщения пользователю
async def send_initial_message(username):
    message = (
            "Привет! Выбери до 5 монет из этого списка:\n\n" +
            ", ".join(all_coins) +
            "\n\nОтветь на это сообщение, перечислив свои выбранные монеты через запятую."
    )
    try:
        await client.send_message(username, message)
        print(f"Сообщение отправлено @{username}")
    except Exception as e:
        print(f"Ошибка при отправке @{username}: {e}")


# Обработка ответа от пользователя
@client.on(events.NewMessage(incoming=True))
async def handle_response(event):
    sender = await event.get_sender()
    username = sender.username
    if not username:
        return  # нельзя сохранить без юзернейма

    text = event.raw_text
    selected = [coin.strip() for coin in text.split(",") if coin.strip() in all_coins]

    if not selected:
        await event.reply("Пожалуйста, выбери монеты из предложенного списка.")
        return

    if len(selected) > 5:
        await event.reply("Нельзя выбрать больше 5 монет.")
        return

    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "INSERT INTO user_choices (username, choices) VALUES (?, ?)",
            (username, ", ".join(selected))
        )
        await db.commit()

    await event.reply(f"Спасибо! Твои монеты сохранены: {', '.join(selected)}")


# Запуск userbot-а
async def main():
    await init_db()
    await client.start()

    # Здесь можно передать юзернеймы, например, полученные от фронта
    usernames = ['example_user1', 'example_user2']  # <-- Заменить на список из фронта
    for username in usernames:
        await send_initial_message(username)

    print("Userbot работает...")
    await client.run_until_disconnected()


if name == "main":
    asyncio.run(main())