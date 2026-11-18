from aiohttp import web
import os
from dotenv import load_dotenv
import asyncio
import logging
#TEST
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# ============== SOZLAMALAR (shu yerni to'ldiring) ==============
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID","0"))
MY_USERNAME = "@IT_Ziyovuddin"  # @ belgisiz, shaxsiy suhbat tugmasi shunga olib boradi

MY_NAME = "Ziyovuddin"
MY_PROFESSION = "Dasturchi"
# =================================================================

logging.basicConfig(level=logging.INFO)

# Token qo'shtirnoq ichiga olindi
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

SITE_TYPES = [
    "Biznes/Korporativ sayt",
    "Onlayn do'kon",
    "Kiyim/Fashion do'kon",
    "Restoran/Kafe sayti",
    "Portfolio sayti",
    "Landing page",
]
OTHER_BTN = "✍️ Boshqa"


class Flow(StatesGroup):
    waiting_intro = State()         # mehmon o'zini tanishtiradi
    waiting_site_type_other = State()  # "Boshqa" bosilsa, turi yoziladi
    waiting_task = State()          # qanday vazifa bajarishi kerak
    waiting_short_info = State()    # nomi va qisqacha ma'lumot
    waiting_phone = State()         # telefon raqami


def intro_text() -> str:
    return (
        f"Assalomu alaykum! 👋\n\n"
        f"Men {MY_NAME}, kasbim — {MY_PROFESSION}.\n\n"
        f"Men sayt va bot yarataman.🛠 \n\n "
        f"Mening Admin Botimga xush kelibsiz! Keling, avval siz bilan tanishib olaylik.\n"
        f"Iltimos, ismingizni va o'zingiz haqida qisqacha yozib bering 🙂\n"
    )


def after_intro_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗣 Shaxsan suhbat qurmoqchiman", callback_data="personal_chat")],
            [InlineKeyboardButton(text="💼 Sayt/bot uchun buyurtma bermoqchiman", callback_data="order_start")],
        ]
    )


def site_type_keyboard() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=t, callback_data=f"site_{i}")] for i, t in enumerate(SITE_TYPES)]
    rows.append([InlineKeyboardButton(text=OTHER_BTN, callback_data="site_other")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def personal_chat_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"👉 {MY_USERNAME} bilan yozishish", url=f"https://t.me/{MY_USERNAME.lstrip('@')}")]
        ]
    )


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(intro_text())
    await state.set_state(Flow.waiting_intro)


@dp.message(Flow.waiting_intro)
async def got_intro(message: Message, state: FSMContext):
    await state.update_data(intro=message.text, guest_name=message.from_user.full_name,
                            guest_username=message.from_user.username)

    # Adminga (sizga) tanishuv ma'lumotini darhol yuborish
    guest_username = f"@{message.from_user.username}" if message.from_user.username else "yo'q"
    await bot.send_message(
        ADMIN_CHAT_ID,
        "🆕 Yangi tanishuv\n\n"
        f"👤 Ism: {message.from_user.full_name}\n"
        f"🔗 Username: {guest_username}\n"
        f"🆔 ID: {message.from_user.id}\n\n"
        f"📝 O'zi haqida yozgani:\n{message.text}",
    )

    await message.answer(
        "Tanishganimdan hursandman! 😁\n\nEndi ishga o'tsak.💼",
        reply_markup=after_intro_keyboard(),
    )
    await state.set_state(None)


@dp.callback_query(F.data == "personal_chat")
async def personal_chat(callback: CallbackQuery):
    await callback.message.edit_text(
        "Albatta! Quyidagi havola orqali shaxsan o'zim bilan suhbat qurishingiz mumkun! 👇",
    )
    await callback.message.answer(
        f"👉 {MY_USERNAME}",
        reply_markup=personal_chat_keyboard(),
    )
    await bot.send_message(
        ADMIN_CHAT_ID,
        f"💬 {callback.from_user.full_name} (@{callback.from_user.username or 'yo‘q'}) "
        f"siz bilan shaxsan suhbat qurishni xohlayapti.",
    )
    await callback.answer()


@dp.callback_query(F.data == "order_start")
async def order_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Sizga qanday sayt yoki bot kerak? Variantlardan birini tanlang 👇")
    await callback.message.answer("Tanlang:", reply_markup=site_type_keyboard())
    await callback.answer()


@dp.callback_query(F.data.startswith("site_"))
async def site_type_chosen(callback: CallbackQuery, state: FSMContext):
    data = callback.data

    if data == "site_other":
        await callback.message.edit_text("Yaxshi, qanday sayt kerakligini o'zingiz yozib qoldiring ✍️")
        await state.set_state(Flow.waiting_site_type_other)
    else:
        idx = int(data.split("_")[1])
        site_type = SITE_TYPES[idx]
        await state.update_data(site_type=site_type)
        await callback.message.edit_text(f"Tanlandi: {site_type}")
        await callback.message.answer("Ushbu sayt yoki bot qanday vazifani bajarishi kerak? Qisqacha yozib bering.")
        await state.set_state(Flow.waiting_task)

    await callback.answer()


@dp.message(Flow.waiting_site_type_other)
async def site_type_other_text(message: Message, state: FSMContext):
    await state.update_data(site_type=message.text)
    await message.answer("Ushbu sayt yoki bot qanday vazifani bajarishi kerak? Qisqacha yozib bering.")
    await state.set_state(Flow.waiting_task)


@dp.message(Flow.waiting_task)
async def got_task(message: Message, state: FSMContext):
    await state.update_data(task=message.text)
    await message.answer(
        "Sayt yoki bot uchun qisqacha ma'lumot bering (masalan: nomi, biznes/soha turi va h.k.)"
    )
    await state.set_state(Flow.waiting_short_info)


@dp.message(Flow.waiting_short_info)
async def got_short_info(message: Message, state: FSMContext):
    await state.update_data(short_info=message.text)
    await message.answer("Bog'lanish uchun telefon raqamingizni qoldiring 📞 \n\n Siz bilan tez orada bog'lanaman.😊")
    await state.set_state(Flow.waiting_phone)


@dp.message(Flow.waiting_phone)
async def got_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    guest_username = f"@{message.from_user.username}" if message.from_user.username else "yo'q"

    summary = (
        "🆕 Yangi buyurtma\n\n"
        f"👤 Mijoz: {message.from_user.full_name} ({guest_username})\n"
        f"🆔 ID: {message.from_user.id}\n\n"
        f"🌐 Sayt turi: {data.get('site_type', '-')}\n"
        f"🎯 Vazifasi: {data.get('task', '-')}\n"
        f"ℹ️ Qisqa ma'lumot: {data.get('short_info', '-')}\n"
        f"📞 Telefon: {message.text}"
    )
    await bot.send_message(ADMIN_CHAT_ID, summary)

    await message.answer(
        "Rahmat! Barcha ma'lumotlaringiz qabul qilindi ✅\n"
        "Tez orada siz bilan bog'lanib shaxsan suhbat quramiz."
    )
    await state.clear()


async def health(request):
    return web.Response(text="OK")


async def start_web():
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    await web.TCPSite(runner, "0.0.0.0", port).start()


async def main():
    await start_web()
    await dp.start_polling(bot)


if name == "__main__":
    asyncio.run(main())