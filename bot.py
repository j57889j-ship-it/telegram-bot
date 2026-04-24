import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Render'dagi Environment Variables'dan tokenni olamiz
API_TOKEN = os.getenv('BOT_TOKEN')

# Loggingni yoqamiz
logging.basicConfig(level=logging.INFO)

# Botni yaratish
if not API_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Ma'lumotlarni saqlash (Xotirada)
test_data = {"keys": None}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("✅ Bot muvaffaqiyatli ishga tushdi!\n\n"
                        "🔑 **Admin uchun:** /set_key abcd... (javoblarni kiriting)\n"
                        "📝 **Foydalanuvchi uchun:** Shunchaki javoblarni yuboring.")

@dp.message_handler(commands=['set_key'])
async def set_test_keys(message: types.Message):
    args = message.get_args()
    if args:
        test_data["keys"] = args.lower()
        await message.answer(f"✅ To'g'ri javoblar saqlandi: `{args.upper()}`")
    else:
        await message.answer("⚠️ Iltimos, javoblarni yozing. Masalan: `/set_key abcd`")

@dp.message_handler()
async def check_answers(message: types.Message):
    user_answers = message.text.lower().replace(" ", "")
    correct_keys = test_data["keys"]

    if not correct_keys:
        await message.answer("❌ Test hali boshlanmagan (Admin kalitlarni kiritmagan).")
        return

    correct_count = 0
    total_questions = len(correct_keys)
    
    # Solishtirish
    for i in range(min(len(user_answers), total_questions)):
        if user_answers[i] == correct_keys[i]:
            correct_count += 1

    foiz = (correct_count / total_questions) * 100
    
    await message.answer(
        f"📊 Sizning natijangiz:\n\n"
        f"✅ To'g'ri: {correct_count} ta\n"
        f"❌ Xato: {total_questions - correct_count} ta\n"
        f"🏁 Jami: {total_questions} ta\n"
        f"📈 Foiz: {foiz:.1f}%"
    )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
