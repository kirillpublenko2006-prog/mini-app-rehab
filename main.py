import os
import uvicorn
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import CommandStart

# =========================
TOKEN = os.getenv("BOT_TOKEN", "8658920992:AAGn2KnQKLlsfC5qrgapvLtSZGBuhM8x23E")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://mini-app-rehab.vercel.app/")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://mini-app-rehab.vercel.app/webhook")
PUBLIC_URL = os.getenv("PUBLIC_URL", "https://mini-app-rehab.vercel.app")
# =========================

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
app = FastAPI()

# ===== /start =====
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text="📊 Открыть мини-приложение",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]],
        resize_keyboard=True
    )
    await message.answer(
        "Добро пожаловать 👋\nНажмите кнопку ниже, чтобы открыть мини-приложение.",
        reply_markup=keyboard
    )

# ===== Web App Data (через кнопку WebApp + tg.sendData) =====
@dp.message(F.web_app_data)
async def web_app_handler(message: types.Message):
    data = message.web_app_data.data
    await message.answer(f"✅ Данные получены:\n\n{data}")

# ===== Webhook endpoint =====
@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        update = await request.json()
        update_obj = types.Update(**update)
        await dp.feed_update(update_obj, bot=bot)
        return {"ok": True}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"ok": False, "error": str(e)}

# ===== Startup / Shutdown =====
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

# ===== Запуск локально =====
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)