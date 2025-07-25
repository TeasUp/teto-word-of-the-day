from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Replace this with your actual bot token
BOT_TOKEN = '7285496835:AAGk-utGF4yZYLSQCBMuV5olti4Ybq99hR8'
MEDIA_PATH = 'media/ban_response.mp4'  # Video file path

async def ban_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    # Only act in group/supergroup and when replying
    if not msg.chat.type.endswith('group') or not msg.reply_to_message:
        return

    # Only allow group admins to use this
    admins = await context.bot.get_chat_administrators(msg.chat.id)
    if msg.from_user.id not in [admin.user.id for admin in admins]:
        return

    # Trigger only if message is exactly "بن"
    if msg.text.strip() != "بن":
        return

    target_id = msg.reply_to_message.from_user.id

    try:
        await context.bot.ban_chat_member(msg.chat.id, target_id)

        # Send video with no caption
        with open(MEDIA_PATH, 'rb') as media:
            await msg.reply_video(InputFile(media))

    except Exception as e:
        await msg.reply_text(f"خطا در بن کردن: {e}")

# Start the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, ban_handler))
app.run_polling()
