from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.filters import CommandStart
from contextlib import asynccontextmanager

BOT_TOKEN = "8658920992:AAGn2KnQKLlsfC5qrgapvLtSZGBuhM8x23E"

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://mini-app-rehab.onrender.com/webhook"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Бот работает 🚀")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(WEBHOOK_URL)
    yield
    await bot.delete_webhook()

app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}
