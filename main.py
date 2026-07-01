from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN = "8629731864:AAFgF2QTrgZW67sjW14zpVFxZFm3UH66nPs"

keyboard = ReplyKeyboardMarkup(
    [
        ["🎮 O'yinni boshlash"],
        ["🏆 Rekordlar"],
        ["❤️ Qo'llab-quvvatlash", "📩 Report"]
    ],
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Assalomu alaykum!\n\n"
        "🤖 Son Topish O'yiniga xush kelibsiz!\n"
        "🏆 Men 0 dan 100 gacha bir son o'ylayman.\n"
        "🧠 Siz esa uni topishga harakat qilasiz.\n\n"
        "👇 Pastdagi tugmalardan birini tanlang!",
        reply_markup=keyboard
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🎮 O'yinni boshlash":
        context.user_data["son"] = random.randint(0, 100)
        context.user_data["urinish"] = 0

        await update.message.reply_text(
            "🎲 Men 0 dan 100 gacha bir son o'yladim.\n"
            "🔍 Sonni kiriting.",
            reply_markup=keyboard
        )
        return

    if text == "🏆 Rekordlar":
        await update.message.reply_text(
            "🏆 Hozircha rekordlar tizimi yo'q.",
            reply_markup=keyboard
        )
        return

    if text == "❤️ Qo'llab-quvvatlash":
        await update.message.reply_text(
            "💳 Donat uchun karta:\n"
            "8600 0000 0000 0000",
            reply_markup=keyboard
        )
        return

    if text == "📩 Report":
        await update.message.reply_text(
            "📩 Muammo bo'lsa adminga yozing.",
            reply_markup=keyboard
        )
        return

    if "son" not in context.user_data:
        await update.message.reply_text(
            "🎮 Avval 'O'yinni boshlash' tugmasini bosing.",
            reply_markup=keyboard
        )
        return

    if not text.isdigit():
        await update.message.reply_text(
            "❌ Faqat son kiriting.",
            reply_markup=keyboard
        )
        return

    son = int(text)
    context.user_data["urinish"] += 1
    random_son = context.user_data["son"]

    if son < random_son:
        await update.message.reply_text(
            "⬆️ Tepaga!",
            reply_markup=keyboard
        )

    elif son > random_son:
        await update.message.reply_text(
            "⬇️ Pastga!",
            reply_markup=keyboard
        )

    else:
        urinish = context.user_data["urinish"]

        await update.message.reply_text(
            f"🎉 Tabriklayman!\n\n"
            f"✅ Siz {random_son} sonini topdingiz.\n"
            f"🏆 Urinishlar soni: {urinish}\n\n"
            f"🔄 Yana o'ynash uchun '🎮 O'yinni boshlash' ni bosing.",
            reply_markup=keyboard
        )

        del context.user_data["son"]
        del context.user_data["urinish"]


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("Bot ishga tushdi...")
app.run_polling()