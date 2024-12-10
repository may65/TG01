from config import TOKEN, KEY
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import requests

API_TOKEN = TOKEN
WEATHER_API_KEY = 'a4c39074d294f4435b58288d9d3c6df5'
CITY_NAME = 'Moscow'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={WEATHER_API_KEY}&units=metric'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def on_startup():
    print('Bot is starting...')


@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Я погодный бот. Используй команду /weather, чтобы получить прогноз погоды.")


@dp.message(Command("help"))
async def send_help(message: Message):
    await message.reply("Я могу предоставить прогноз погоды. Попробуй команду /weather.")


@dp.message(Command("weather"))
async def get_weather(message: Message):
    response = requests.get(WEATHER_URL)
    data = response.json()
    if data.get("cod") != 200:
        await message.reply("Не удалось получить данные о погоде.")
        return

    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    weather_report = f"В городе {CITY_NAME} сейчас {temp}°C, {description}."
    await message.reply(weather_report)


async def main():
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
