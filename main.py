import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from config import BOT_TOKEN
from database import hesap_ekle, hesaplari_getir, hesap_sil
from checker import kontrol_et

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

beklemede = {}

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Hesap Ekle")],
        [KeyboardButton(text="📋 Takip Listem")],
        [KeyboardButton(text="❌ Hesap Sil")]
    ],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🔔 Instagram Monitor Bot\n\n"
        "Bir işlem seç.",
        reply_markup=menu
    )


@dp.message(F.text == "➕ Hesap Ekle")
async def ekle(message: Message):
    beklemede[message.from_user.id] = "ekle"
    await message.answer("Instagram kullanıcı adını gönder.")


@dp.message(F.text == "📋 Takip Listem")
async def liste(message: Message):
    hesaplar = hesaplari_getir(message.from_user.id)

    if not hesaplar:
        await message.answer("Takip listen boş.")
        return

    yazi = "📋 Takip Listen\n\n"

    for h in hesaplar:
        yazi += f"• @{h[0]}\n"

    await message.answer(yazi)


@dp.message(F.text == "❌ Hesap Sil")
async def sil(message: Message):
    beklemede[message.from_user.id] = "sil"
    await message.answer("Silmek istediğin kullanıcı adını gönder.")


@dp.message()
async def cevap(message: Message):

    uid = message.from_user.id

    if uid not in beklemede:
        return

    username = message.text.replace("@", "").strip()

    if beklemede[uid] == "ekle":
        hesap_ekle(uid, username)
        await message.answer(f"✅ @{username} eklendi.")

    elif beklemede[uid] == "sil":
        hesap_sil(uid, username)
        await message.answer(f"🗑️ @{username} silindi.")

    del beklemede[uid]


async def main():
    asyncio.create_task(kontrol_et(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
