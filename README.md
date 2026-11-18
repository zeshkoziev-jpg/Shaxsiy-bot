# Ziyovuddin — tanishtiruv/buyurtma boti

## 1. Botni yaratish
1. Telegramda **@BotFather** ga yozing → `/newbot` → nom va username bering.
2. Sizga beriladigan **token**ni nusxalab oling.

## 2. O'z ID raqamingizni olish
1. Telegramda **@userinfobot** ga yozing.
2. U sizga raqamli **ID** qaytaradi (masalan: `123456789`).

## 3. Kodni sozlash
`bot.py` faylining yuqori qismida:
```python
BOT_TOKEN = "SIZNING_BOT_TOKENINGIZ"   # BotFather'dan olingan token
ADMIN_CHAT_ID = 123456789              # @userinfobot'dan olingan ID
MY_USERNAME = "IT_Ziyovuddin"          # shaxsiy username
```
shu joylarni o'zingiznikiga almashtiring.

> ⚠️ Muhim: botni ishga tushirgandan so'ng, avval **o'zingiz botga `/start` yozib**, keyin odatdagidek tanishuv jarayonidan o'ting — shunda bot ADMIN_CHAT_ID to'g'ri ekanini tekshirasiz (xabarlar sizga kelishi kerak).

## 4. Mahalliy kompyuterda ishga tushirish
```bash
pip install -r requirements.txt
python bot.py
```

## 5. Bepul hostingga joylash (Render.com tavsiya etiladi)
1. Kodni GitHub'ga yuklang (yangi repository yarating, shu 3 faylni joylang).
2. [render.com](https://render.com) da ro'yxatdan o'ting → **New +** → **Background Worker** tanlang.
3. GitHub repongizni ulang.
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python bot.py`
6. Deploy qiling — bot 24/7 ishlab turadi (bepul tarifda ba'zan sekinroq bo'lishi mumkin, lekin ishlayveradi).

Eslatma: token va ID'ni kodga yozish o'rniga xavfsizroq usul — Render'ning **Environment Variables** bo'limiga qo'yib, kodda `os.environ["BOT_TOKEN"]` orqali o'qish. Agar shunday qilishni xohlasangiz, ayting — kodni moslab beraman.

## Oqim qisqacha
1. Mehmon `/start` bosadi → siz haqingizda qisqa matn + o'zini tanishtirish so'raladi.
2. U yozgan matn darhol sizning shaxsiy chatingizga yuboriladi.
3. Mehmonga 2 ta tugma chiqadi:
   - **Shaxsan suhbat** → sizning @username'ingizga link.
   - **Sayt/ish buyurtmasi** → sayt turi (6 ta tugma + "Boshqa") → vazifa → qisqa ma'lumot → telefon raqami → barchasi tartib bilan sizga yuboriladi.
